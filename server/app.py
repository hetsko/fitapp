import logging
import functools
import threading
import itertools
import webbrowser

from flask import Flask, jsonify, request, redirect
from wsgiref.simple_server import make_server


logger = logging.getLogger(__name__)
unique_id = itertools.count()

fitapps_ports = {}


class FitApp:
    def __init__(self, port=5050, open_browser=True):
        self._ids = []
        self._get_data = lambda _: {'x': []}
        self._get_metadata = lambda _: 'n/a'

        self._flask_app = create_flask(self)
        try:
            self._server = make_server('127.0.0.1', port, self._flask_app)
        except OSError:
            raise RuntimeError(f'Port {port} already in use, try another one or 0')

        logger.info(f'App is running on {self.address}')
        self._server_thread = threading.Thread(
            target=self._server.serve_forever,
            name=f'FitApp-server-{next(unique_id)}',
            daemon=True,
        )
        self._server_thread.start()
        if open_browser:
            self.open_browser()

    def _wait_forever(self):
        """Block the main thread and keep the server up."""
        self._server_thread.join()

    def _stop(self):
        """Signal the server to stop and wait until its thread is finished."""
        self._server.shutdown()
        self._server_thread.join()

    @property
    def address(self):
        return 'http://{}:{}/'.format(*self._server.server_address)

    def open_browser(self):
        """Opens the app in your default browser."""
        webbrowser.open_new_tab(self.address)

    # def set_data(self, data):
    #     pass

    # def set_metadata(self, data):
    #     pass

    def set_ids(self, ids):
        self._ids = list(ids)

    def callback_data(self, get_data):
        self._get_data = get_data

    def callback_metadata(self, get_metadata):
        self._get_metadata = get_metadata


def get_fitapp(port:int=5050, open_browser:bool=True) -> FitApp:
    """Create a new FitApp listening at given port. Any subsequent calls to this
    function with the same `port` parameter return the original app instance.
    """
    if port not in fitapps_ports:
        fitapps_ports[port] = FitApp(port=port, open_browser=open_browser)
    return fitapps_ports[port]


def json_required(keys):
    def decorator(f):
        @functools.wraps(f)
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

def create_flask(fitapp):
    app = Flask(__name__, '/', '../public')

    @app.route('/')
    def root():
        return redirect('/index.html')

    @app.route('/ids')
    def ids():
        return jsonify(ids=fitapp._ids)

    @app.route('/metadata')
    @json_required(['id'])
    def metadata(json):
        if json['id'] not in fitapp._ids:
            return jsonify(ok=False, error=f'Id \'{json["id"]}\' not found'), 404

        try:
            metadata = fitapp._get_metadata(json['id'])
        except Exception as e:
            return jsonify(ok=False, error='exception',
                        exception=f'{type(e).__name__}: {str(e)}'), 500

        if not isinstance(data, str):
            return jsonify(ok=False, error=f'get_metadata(): must return str'), 500
        else:
            return jsonify(ok=True, metadata=metadata), 200

    @app.route('/data')
    @json_required(['id'])
    def data(json):
        if json['id'] not in fitapp._ids:
            return jsonify(ok=False, error=f'Id \'{json["id"]}\' not found'), 404

        try:
            data = fitapp._get_data(json['id'])
        except Exception as e:
            return jsonify(ok=False, error='exception',
                        exception=f'{type(e).__name__}: {str(e)}'), 500

        if not isinstance(data, dict):
            return jsonify(ok=False, error=f'get_data(): must return dict'), 500
        if not any(set(data) == t for t in [{'x'}, {'x', 'y'}, {'x', 'y', 'yerr'}]):
            return jsonify(ok=False, error=f'get_data(): returned dict with invalid keys'), 500
        else:
            return jsonify(ok=True, data=data), 200

    return app
