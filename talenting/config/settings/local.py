from .base import *

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.elasticbeanstalk.com',
    '.yabi.kr',
]


DATABASES = config_secret_common['django']['databases']

SECRET_KEY = config_secret_common['django']['secret_key']
