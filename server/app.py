import logging
import functools
import webbrowser
import os
import contextlib
import threading
import inspect

from wsgiref.simple_server import make_server
from flask import Flask, jsonify, request, redirect

import numpy
from scipy.optimize import curve_fit


_logger = logging.getLogger(__name__)

fitapps_ports = {}


def get_fitapp(port=5050, open_browser=True, local=True, http_log=False, data_cache=16):
    """Create a new FitApp listening at given port. Any subsequent calls to this
    function with the same `port` parameter return the original app instance.
    """
    if port not in fitapps_ports:
        fitapps_ports[port] = FitApp(port, open_browser, local, http_log, data_cache)
    else:
        _logger.info(
            f'Access an existing app on {fitapps_ports[port].address}')
    return fitapps_ports[port]


class Data:
    """Utility class that converts list/numpy/xarray data to a universal
    data format, which can be serialized and sent to the web browser.

    Callback get_data() registered in FitApp must return instace of Data.
    """

    def __init__(self, x, y=None, yerr=None):
        """Specify either (x), (x, y) or (x, y, yerr). Use instance/s of
            - list
            - numpy.ndarray
            - xarray.DataArray
        """
        self.x = numpy.asarray(x)
        self.y = numpy.asarray(y) if y is not None else y
        self.yerr = numpy.asarray(yerr) if yerr is not None else yerr

    def __repr__(self):
        variables = (
            v for v in ("x", "y", "yerr") if getattr(self, v) is not None
        )
        return f'Data({", ".join(variables)})'

    def todict(self):
        return {
            key: val.tolist()
            for key, val in zip(('x', 'y', 'yerr'), (self.x, self.y, self.yerr))
            if val is not None
        }

    def select(self, indices):
        """Return a new instance of Data with selected a subset of data.
        Analogous to numpy.ndarray: a[[1, 2, 4]]
        """
        return Data(
            x=self.x[indices],
            y=self.y[indices] if self.y is not None else self.y,
            yerr=self.yerr[indices] if self.yerr is not None else self.yerr,
        )


class FitApp:
    def __init__(self, port=5050, open_browser=True, local=True, http_log=False, data_cache=16):
        self._labels = []
        self._labels_str = {}
        self._fitfunc = None
        self._fitfunc_params = []
        self._get_metadata = lambda _: 'n/a'
        self._get_data = lambda _: Data(x=[])
        self._get_guess = lambda _: len(self._fitfunc_params) * [1]

        self._lru_cache = data_cache
        self._last_fitresults = None

        self._flask_app = self._init_flask()
        try:
            self._server = make_server(
                '127.0.0.1' if local else '0.0.0.0', port, self._flask_app,
            )
        except OSError:
            raise RuntimeError(
                f'Port {port} already in use, try another one or 0')

        if http_log:
            run = self._server.serve_forever
        else:
            def run():
                with open(os.devnull, 'w') as null:
                    with contextlib.redirect_stderr(null):
                        self._server.serve_forever()
        self._server_thread = threading.Thread(
            target=run,
            name=f'FitApp-server-p{port}',
            daemon=True,
        )
        self._server_thread.start()

        _logger.info(f'New app is running on {self.address}')
        if open_browser:
            self.open_browser()

    def _init_flask(self):
        app = Flask(__name__, '/', '../public')

        @app.route('/')
        def root():
            return redirect('/index.html')

        @app.route('/ids')
        def ids():
            return jsonify(ids=list(self._labels_str))

        @app.route('/data.meta', methods=['POST'])
        @json_required(['id'])
        def metadata(json):
            if json['id'] not in self._labels_str:
                return jsonify(ok=False, error=f'Id \'{json["id"]}\' not found'), 404

            try:
                metadata = self._get_metadata(json['id'])
            except Exception as e:
                _logger.error(f'/data.meta: {type(e).__name__}: {str(e)}')
                return jsonify(ok=False, error='exception',
                               exception=f'{type(e).__name__}: {str(e)}'), 500

            if not isinstance(metadata, str):
                error = 'Callback get_metadata() must return str'
                _logger.error(error)
                return jsonify(ok=False, error=error), 500
            else:
                return jsonify(ok=True, metadata=metadata), 200

        @app.route('/data.data', methods=['POST'])
        @json_required(['id'])
        def data(json):
            if json['id'] not in self._labels_str:
                return jsonify(ok=False, error=f'Id \'{json["id"]}\' not found'), 404

            try:
                data = self._get_data(json['id'])
            except Exception as e:
                _logger.error(f'/data.data: {type(e).__name__}: {str(e)}')
                return jsonify(ok=False, error='exception',
                               exception=f'{type(e).__name__}: {str(e)}'), 500
            if not isinstance(data, Data):
                error = 'Callback get_data() must return instance of Data'
                _logger.error(error)
                return jsonify(ok=False, error=error), 500
            return jsonify(ok=True, data=data.todict()), 200

        @app.route('/fit.meta', methods=['POST'])
        @json_required(['id'])
        def fit_metadata(json):
            if json['id'] not in self._labels_str:
                return jsonify(ok=False, error=f'Id \'{json["id"]}\' not found'), 404
            if self._fitfunc is None:
                return jsonify(ok=False, error='No fit model was not specified'), 400

            try:
                guess = numpy.asarray(self._get_guess(json['id']))
                metadata = {
                    'args': guess.tolist(),
                    'params': self._fitfunc_params,
                }
            except Exception as e:
                _logger.error(f'/fit.meta: {type(e).__name__}: {str(e)}')
                return jsonify(ok=False, error='exception',
                               exception=f'{type(e).__name__}: {str(e)}'), 500
            return jsonify(ok=True, metadata=metadata), 200

        @app.route('/fit.data', methods=['POST'])
        @json_required(['fitArgs', 'start', 'stop', 'num'])
        def fit_data(json):
            if self._fitfunc is None:
                return jsonify(ok=False, error='No fit model was not specified'), 400
            if len(json['fitArgs']) != len(self._fitfunc_params):
                return jsonify(
                    ok=False,
                    error=f'Invalid length of fitArgs ({len(json["fitArgs"])})',
                ), 400

            try:
                x = numpy.linspace(json['start'], json['stop'], json['num'])
                data = Data(x=x, y=self._fitfunc(x, *json['fitArgs']))
            except Exception as e:
                _logger.error(f'/fit.data: {type(e).__name__}: {str(e)}')
                return jsonify(ok=False, error='exception',
                               exception=f'{type(e).__name__}: {str(e)}'), 500
            return jsonify(ok=True, data=data.todict()), 200

        @app.route('/fit.calculate', methods=['POST'])
        @json_required(['id', 'fitArgs', 'selected'])
        def fit_calculate(json):
            if json['id'] not in self._labels_str:
                return jsonify(ok=False, error=f'Id \'{json["id"]}\' not found'), 404
            if self._fitfunc is None:
                return jsonify(ok=False, error='No fit model was not specified'), 400
            if json['fitArgs'] and len(json['fitArgs']) != len(self._fitfunc_params):
                return jsonify(
                    ok=False,
                    error=f'Invalid length of fitArgs ({len(json["fitArgs"])})',
                ), 400
            elif json['fitArgs']:
                json['fitArgs'] = numpy.asarray(json['fitArgs'])

            try:
                data = self._get_data(json['id'])
                if json['selected']:
                    json['selected'] = numpy.asarray(json['selected'])
                else:
                    json['selected'] = numpy.arange(len(data.x))
                data = data.select(json['selected'])
                results = self._fit_data(
                    self._fitfunc, data, guess=json['fitArgs'])
            except Exception as e:
                _logger.error(f'/fit.calculate: {type(e).__name__}: {str(e)}')
                return jsonify(ok=False, error='exception',
                               exception=f'{type(e).__name__}: {str(e)}'), 500

            self._last_fitresults = {
                **results,
                'params': numpy.array(self._fitfunc_params),
                'label': self._labels_str[json['id']],
                'guess': json['fitArgs'],
                'data': data,
                'selected': json['selected'],
            }

            serializable = {
                k: a.tolist() for k, a in results.items()
                if numpy.isfinite(a).all()
            }
            for key in results:
                serializable.setdefault(key, None)
            return jsonify(ok=True, results=serializable), 200

        return app

    def _wait_forever(self):
        """Block the main thread and keep the server up."""
        self._server_thread.join()

    def _stop(self):
        """Signal the server to stop and wait until its thread is finished."""
        self._server.shutdown()
        self._server_thread.join()

    @ staticmethod
    def _fit_data(f, data, guess=None):
        if data.y is None:
            raise RuntimeError('Cannot fit data without y coordinates')
        opt, std = curve_fit(
            f,
            numpy.asarray(data.x),
            numpy.asarray(data.y),
            sigma=None if data.yerr is None else numpy.asarray(data.yerr),
            p0=guess
        )
        return {
            'args': opt,
            'argsErr': numpy.sqrt(numpy.diag(std))
        }

    @property
    def address(self):
        """Address of the web interface."""
        return 'http://{}:{}/'.format(*self._server.server_address)

    def open_browser(self):
        """Opens the app in your default browser."""
        webbrowser.open_new_tab(self.address)

    @property
    def labels(self):
        """List of unique labels for your datasets. Note that the labels need
        to stay unique when converted to text using str(), as they are
        internally stored as text. To avoid this issue, use base types and
        simple objects such as list or dict.

        Labels are shown in the webapp (converted to text) and passed as an
        argument to the callback functions (in the original non-text form).
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = list(labels)
        self._labels_str = {str(l): l for l in self._labels}

    @property
    def fit_results(self):
        """Dict with results from the most recent fit calculation. Returns None
        when there was no calculation yet. Keys:

        'label' - the label for the data
        'data' - the fitted data as an instance of Data (after selection)
        'selected' - array of indices of points that were selected
        'guess' - array of initial values of the fit parameters
        'args' - array of optimized values of the fit parameters
        'argsErr' - array of errors estimated from the covariance matrix
        'params' - names of the fit parameters (as specified by the fit func)
        """
        if self._last_fitresults:
            return dict(self._last_fitresults)
        else:
            return None

    # def set_data(self, data):
    #     pass

    # def set_metadata(self, data):
    #     pass

    def set_fitfunc(self, func):
        """Set function, which represents the fit model. I.e. the first
        argument of scipy.optimize.curve_fit
        """
        self._fitfunc = func
        self._fitfunc_params = list(inspect.signature(func).parameters)[1:]

    def callback_metadata(self, get_metadata):
        """Set callback for additional information about data with signature:

        def get_metadata(label: any) -> str
        """
        self._get_metadata = lambda l: get_metadata(self._labels_str[l])

    def callback_data(self, get_data):
        """Set callback for data with signature:

        def get_data(label: any) -> Data
        """
        self._get_data = lambda l: get_data(self._labels_str[l])
        if self._lru_cache:
            self._get_data = functools.lru_cache(
                self._lru_cache)(self._get_data)

    def callback_guess(self, get_guess):
        """Set callback for initial values of the fit parameters with signature:

        def get_guess(label: any) -> array_like
        """
        self._get_guess = lambda l: get_guess(self._labels_str[l])


def json_required(keys):
    def decorator(f):
        @ functools.wraps(f)
        def wrapped(*args, **kwargs):
            json = request.get_json()
            if not json:
                return jsonify(error='Bad request'), 400
            missing = [k for k in keys if k not in json]
            if len(missing) > 0:
                return jsonify(error=f'Missing keys: {missing}'), 400
            return f(json, *args, **kwargs)
        return wrapped
    return decorator
