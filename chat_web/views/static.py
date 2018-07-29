from aiohttp import web
import logging
from pathlib import Path
import sys


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


@routes.get('/{path:.*}')
async def frontend_static(req):
    path = req.url.path
    logger.info('Static path: %r', path)
    mod_name = __name__.split('.')[0]
    mod_path = sys.modules[mod_name].__path__[0]
    static_dir = Path(mod_path) / 'frontend_static'
    if not static_dir.is_dir():
        logger.error('Not a directory: %r', static_dir)
        raise web.HTTPInternalServerError(text='Cannot find directory frontend_static')
    static_path = (static_dir / path.strip('/')).resolve()
    logger.debug('Static file path: %s', static_path)
    static_path.relative_to(static_dir)
    if static_path.is_dir():
        static_path = static_path / 'index.html'
    if not static_path.is_file():
        raise web.HTTPNotFound()
    return web.Response(
        body=static_path.read_bytes(),
        content_type=get_content_type_from_filename(static_path.name))


def get_content_type_from_filename(name):
    if name.endswith('.html'):
        return 'text/html'
    if name.endswith('.js'):
        return 'application/javascript'
    raise Exception(f'Unknown file name: {name}')
