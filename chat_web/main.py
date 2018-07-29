from aiohttp import web
import argparse
import logging
import os

from .configuration import Configuration
from .views import routes


log_format = '%(asctime)s [%(process)d %(threadName)s] %(name)-25s %(levelname)5s: %(message)s'


def get_app(conf):
    app = web.Application()
    app['conf'] = conf
    setup_session(app)
    app.add_routes(routes)
    return app


def setup_session(app):
    from aiohttp_session import setup
    from aiohttp_session.cookie_storage import EncryptedCookieStorage
    from hashlib import sha256
    session_secret_hash = sha256(app['conf'].session_secret.encode()).digest()
    storage = EncryptedCookieStorage(session_secret_hash)
    setup(app, storage)


def chat_web_main():
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int)
    args = p.parse_args()
    port = int(args.port or os.environ.get('PORT') or 5000)
    logging.basicConfig(
        format=log_format,
        level=logging.DEBUG)
    conf = Configuration()
    app = get_app(conf)
    web.run_app(app, port=port)
