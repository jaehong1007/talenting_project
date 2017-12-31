
from .base import *

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.elasticbeanstalk.com',
    '.yabi.kr',
]

config_secret_local = json.loads(open(CONFIG_SECRET_LOCAL_FILE).read())

DATABASES = config_secret_local['django']['databases']

