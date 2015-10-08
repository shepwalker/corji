import os


class Config(object):
    CACHE_DIR = os.getenv('CACHE_DIR', './.cache')
    DEBUG = os.getenv('DEBUG', False)
    LOG_NAME = os.getenv('LOG_NAME', 'corji.log')
    LOG_PATH = os.getenv('LOG_PATH', './.logs')
    SPREADSHEET_URL = os.getenv('SPREADSHEET_URL', '')
    
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'SUPER_NOT_VALID_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'SUPER_NOT_VALID_SECRET')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'SUPER_NOT_VALID_REGION')
    AWS_S3_CACHE_BUCKET_NAME = os.getenv('AWS_S3_CACHE_BUCKET_NAME', 'SUPER_NOT_VALID_BUCKET')
    REMOTE_CACHE_RETRIEVE_ENABLED = True if (os.getenv('REMOTE_CACHE_RETRIEVE_ENABLED') == "TRUE") else False
    REMOTE_CACHE_POPULATE_ENABLED = True if (os.getenv('REMOTE_CACHE_POPULATE_ENABLED') == "TRUE") else False