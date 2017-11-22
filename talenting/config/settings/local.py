from .base import *

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.elasticbeanstalk.com',
    '.yabi.kr',
]
CONFIG_SECRET_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'database.json')
database = json.loads(open(CONFIG_SECRET_COMMON_FILE).read())


DATABASES = database['databases']

SECRET_KEY = config_secret_common['django']['secret_key']

