import logging
import functools

from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer

logger = logging.getLogger(__name__)


class FitApp:
    def __init__(self, port=5050):
        self.port = port
        self.address = f'http://127.0.0.1:{port}'

        self._ids = []
        self._get_data = lambda _: {'x': []}
        self._get_metadata = lambda _: 'n/a'

        self._flask_app = create_flask(self)
        self._server = WSGIServer(('', port), self._flask_app)

        self._server.serve_forever()
        logger.info(f'App is running on {self.address}')

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
