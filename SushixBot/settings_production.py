import dj_database_url
from SushixBot.settings import *

DATABASES['default'] = dj_database_url.config()

ALLOWED_HOSTS = [
    'api.sushix.tv',
    'sushixtv-backend.herokuapp.com'
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'https://www.sushix.tv',
    'http://www.sushix.tv',
    'https://sushix.tv',
    'http://sushix.tv',
]

DEBUG = False

DEVELOPER_MODE = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
