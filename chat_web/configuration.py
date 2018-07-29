import logging
import os
from secrets import token_hex


logger = logging.getLogger(__name__)


class Configuration:

    def __init__(self):
        self.google_oauth2 = OAuth2('google')
        self.fb_oauth2 = OAuth2('fb')
        self.session_secret = os.environ.get('SESSION_SECRET') or token_hex()
        self.allow_dev_login = bool(os.environ.get('ALLOW_DEV_LOGIN'))


class OAuth2:

    def __init__(self, prefix):
        get = lambda key: os.environ[f'{prefix}_OAUTH2_{key}'.upper()]
        try:
            self.client_id = get('client_id')
        except KeyError:
            logger.debug('%s client_id not configured', prefix)
            self.client_id = None
        else:
            self.client_secret = get('client_secret')
            self.callback_url = get('callback_url')

    def __bool__(self):
        return bool(self.client_id and self.client_secret and self.callback_url)
