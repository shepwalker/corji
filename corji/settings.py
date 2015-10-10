import os


class Config(object):
    # General variables.
    DEBUG = os.getenv('DEBUG', False)

    # Data variables.
    CACHE_DIR = os.getenv('CACHE_DIR', './.cache')
    FALLBACK_IMAGE = os.getenv('FALLBACK_IMAGE', 'https://s-media-cache-ak0.pinimg.com/736x/49/2a/7f/492a7ff287bdc50d34a4989ab83d9830.jpg')
    SPREADSHEET_URL = os.getenv('SPREADSHEET_URL', '')
    REMOTE_CACHE_RETRIEVE = True if (os.getenv('REMOTE_CACHE_RETRIEVE') == "TRUE") else False
    REMOTE_CACHE_POPULATE = True if (os.getenv('REMOTE_CACHE_POPULATE') == "TRUE") else False


    # Operational variables.
    LOG_NAME = os.getenv('LOG_NAME', 'corji.log')
    LOG_PATH = os.getenv('LOG_PATH', './.logs')
    LOGGER_NAME = "FLASK_APP_LOGGER"

    # Frontend variables.
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', '')

    # AWS variables.    
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'SUPER_NOT_VALID_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'SUPER_NOT_VALID_SECRET')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'SUPER_NOT_VALID_REGION')
    AWS_S3_CACHE_BUCKET_NAME = os.getenv('AWS_S3_CACHE_BUCKET_NAME', 'SUPER_NOT_VALID_BUCKET')
