'''
Docs:

https://requests-oauthlib.readthedocs.io/en/latest/examples/facebook.html
https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html
'''

from aiohttp import web
from aiohttp_session import get_session
import logging
import asyncio
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix


logger = logging.getLogger(__name__)

routes = web.RouteTableDef()


fb_authorization_base_url = 'https://www.facebook.com/dialog/oauth'
fb_token_url = 'https://graph.facebook.com/oauth/access_token'
fb_me_url = 'https://graph.facebook.com/me?fields=id,name,email'

google_authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
google_token_url = "https://www.googleapis.com/oauth2/v4/token"
google_user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'


@routes.get('/auth/session')
async def debug_session(req):
    '''
    For debug purposes.
    Maybe should be disabled in production.
    '''
    session = await get_session(req)
    return web.json_response(dict(session))


@routes.get('/auth/methods')
async def auth_methods(req):
    conf = req.app['conf']
    methods = {
        'fb': '/auth/facebook' if conf.fb_oauth2 else None,
        'google': '/auth/google' if conf.fb_oauth2 else None,
        'dev': '/auth/dev' if conf.allow_dev_login else None,
    }
    if not any(methods.values()):
        raise web.HTTPInternalServerError(text='No auth methods configured')
    return web.json_response(methods)


@routes.get('/auth/dev')
async def dev_login(req):
    name = req.query['name'].strip()
    conf = req.app['conf']
    if not conf.allow_dev_login:
        raise web.HTTPForbidden()
    logger.info('Logging in as dev user: %r', name)
    session = await get_session(req)
    session['user'] = {
        'provider': 'dev',
        'name': name,
        'email': f'{name}@example.com'.replace(' ', '.'),
    }
    raise web.HTTPFound('/chat')


def get_fb_oauth2_session(conf):
    from requests_oauthlib import OAuth2Session
    from requests_oauthlib.compliance_fixes import facebook_compliance_fix
    if not conf.client_id:
        raise web.HTTPInternalServerError(text='credentials not configured')
    sess = OAuth2Session(client_id=conf.client_id, redirect_uri=conf.callback_url)
    sess = facebook_compliance_fix(sess)
    return sess


@routes.get('/auth/facebook')
async def fb_redirect(req):
    session = await get_session(req)
    session['user'] = None
    conf = req.app['conf'].fb_oauth2
    oauth2_sess = get_fb_oauth2_session(conf)
    authorization_url, state = oauth2_sess.authorization_url(fb_authorization_base_url)
    session['oauth2_state'] = state
    logger.debug('Redirecting to %s', authorization_url)
    raise web.HTTPFound(authorization_url)


@routes.get('/auth/facebook/callback')
async def fb_callback(req):
    session = await get_session(req)
    if req.query['state'] != session['oauth2_state']:
        raise web.HTTPForbidden(text='state mismatch')
    del session['oauth2_state']
    conf = req.app['conf'].fb_oauth2

    def fetch():
        oauth2_sess = get_fb_oauth2_session(conf)
        token = oauth2_sess.fetch_token(
            fb_token_url, client_secret=conf.client_secret, code=req.query['code'])
        r = oauth2_sess.get(fb_me_url)
        r.raise_for_status()
        me = r.json()
        return token, me

    token, me = await asyncio.get_event_loop().run_in_executor(None, fetch)
    logger.info('FB me: %r', me)
    session['user'] = {
        'provider': 'fb',
        'fb_token': token,
        'fb_id': me['id'],
        'name': me['name'],
        'email': me['email'],
    }
    raise web.HTTPFound('/chat')


def get_google_oauth2_session(conf):
    from requests_oauthlib import OAuth2Session
    scope = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
    sess = OAuth2Session(conf.client_id, scope=scope, redirect_uri=conf.callback_url)
    return sess


@routes.get('/auth/google')
async def google_redirect(req):
    session = await get_session(req)
    session['user'] = None
    conf = req.app['conf'].google_oauth2
    oauth2_sess = get_google_oauth2_session(conf)
    authorization_url, state = oauth2_sess.authorization_url(google_authorization_base_url)
    # access_type="offline", prompt="select_account")
    session['oauth2_state'] = state
    logger.debug('Redirecting to %s', authorization_url)
    raise web.HTTPFound(authorization_url)


@routes.get('/auth/google/callback')
async def google_callback(req):
    session = await get_session(req)
    if req.query['state'] != session['oauth2_state']:
        raise web.HTTPForbidden(text='state mismatch')
    del session['oauth2_state']
    conf = req.app['conf'].google_oauth2

    def fetch():
        oauth2_sess = get_google_oauth2_session(conf)
        token = oauth2_sess.fetch_token(google_token_url,
            client_secret=conf.client_secret, code=req.query['code'])
        r = oauth2_sess.get(google_user_info_url)
        r.raise_for_status()
        me = r.json()
        return token, me

    token, me = await asyncio.get_event_loop().run_in_executor(None, fetch)
    session['user'] = {
        'provider': 'google',
        'google_token': token,
        'google_id': me['id'],
        'name': me['name'],
        'email': me['email'],
    }
    raise web.HTTPFound('/chat')
