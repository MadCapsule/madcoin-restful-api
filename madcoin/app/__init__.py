import os
import bitcoinrpc
from flask import Flask
from flask import jsonify, request
from flask import Flask, current_app
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

__all__ = ['make_json_app']

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have applications/json content
    type, and will contain JSON like this (just an example)
    {"message":"405: Method Not Allowed"}

    More here: http://flask.pocoo.org/snippets/83/
    """
    def make_json_error(ex):
        response = jsonify(
            message=str(ex),
            code=(ex.code if isinstance(ex, HTTPException) else 500))

        response.status_code = \
            (ex.code if isinstance(ex, HTTPException) else 500)

        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error
    return app

def get_config_for_subdomain(subdomain):
    if subdomain == 'bitcoin':
        return 'config/bitcoin.cfg'
    elif subdomain == 'litecoin':
        return 'config/litecoin.cfg'
    else:
        return None

def create_app(cfg=None):
    app = make_json_app(__name__)
    load_config(app, cfg)
    from app.views import api
    app.register_blueprint(api)
    return app

def load_config(app, cfg):
    app.config.from_pyfile('config/default.cfg')

    if cfg is None and 'MADCOIN_CFG' in os.environ:
        cfg = os.environ['MADCOIN_CFG']

    if cfg is not None:
        app.config.from_pyfile(cfg)
