#!venv/bin/python
import sys
from threading import Lock
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
from werkzeug.wsgi import pop_path_info, peek_path_info
from app import create_app, get_config_for_subdomain


class SubdomainDispatcher(object):

    def __init__(self, domain, create_app):
        self.domain = domain
        self.create_app = create_app
        self.lock = Lock()
        self.instances = {}

    def get_application(self, host):
        host = host.split(':')[0]
        assert host.endswith(self.domain), 'Configuration error'
        subdomain = host[:-len(self.domain)].rstrip('.')
        with self.lock:
            app = self.instances.get(subdomain)
            if app is None:
                app = self.create_app(subdomain)
                self.instances[subdomain] = app
            return app

    def __call__(self, environ, start_response):
        app = self.get_application(environ['HTTP_HOST'])
        return app(environ, start_response)


def make_app(subdomain):
    config = get_config_for_subdomain(subdomain)
    if config is None:
        return NotFound()

    return create_app(config)

app = SubdomainDispatcher('mad.local', make_app)

run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True,
           use_evalex=True)
