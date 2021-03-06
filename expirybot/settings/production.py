from .common import *

import os

from django.core.exceptions import ImproperlyConfigured

import dj_database_url

try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    raise ImproperlyConfigured(
        "In production mode you must specify the `SECRET_KEY` environment "
        "variable. If you're _definitely not_ running in production it's safe "
        "to set this to something insecure, eg `export SECRET_KEY=foo`")
assert len(SECRET_KEY) > 20, "Bad (short) secret key: {}".format(SECRET_KEY)

DEBUG = False

ALLOWED_HOSTS = [
    'www.expirybot.com',
    'rwsjgwuykifsy6jh.onion',
]

# To use SECURE_PROXY_SSL_HEADER you *must* make sure
#
# 1. this app is reverse proxied behind an SSL-terminating proxy
# 2. the proxy strips HTTP_X_FORWARDED_PROTO from any requests it receives
# 3. the proxy passes HTTP_X_FORWARDED_PROTO: https only for its SSL config

SECURE_PROXY_SSL_HEADER = ('X-Forwarded-Proto', 'https')

SERVE_STATIC_FILES = False

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {'default': db_from_env}
