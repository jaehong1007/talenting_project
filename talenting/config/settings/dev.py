from .base import *

config_secret_dev = json.loads(open(
    CONFIG_SECRET_DEV_FILE).read())

# Databases
DATABASES = config_secret_dev['django']['databases']

# AWS
AWS_ACCESS_KEY_ID = config_secret_dev['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret_dev['aws']['secret_access_key']
AWS_S3_BUCKET_NAME = config_secret_dev['aws']['s3_bucket_name']
AWS_S3_REGION_NAME = config_secret_dev['aws']['s3_region_name']


