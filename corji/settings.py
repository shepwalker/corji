import os


class Config(object):
    # General variables.
    DEBUG = os.getenv('DEBUG', False)

    # Data variables.
    CACHE_DIR = os.getenv('CACHE_DIR', './.cache')
    FALLBACK_IMAGE = os.getenv('FALLBACK_IMAGE', 'https://s-media-cache-ak0.pinimg.com/736x/49/2a/7f/492a7ff287bdc50d34a4989ab83d9830.jpg')
    SPREADSHEET_URL = os.getenv('SPREADSHEET_URL', '')

    # Operational variables.
    LOG_NAME = os.getenv('LOG_NAME', 'corji.log')
    LOG_PATH = os.getenv('LOG_PATH', './.logs')

    # Frontend variables.
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', '')
