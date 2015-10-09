import os


class Config(object):
    # General variables.
    DEBUG = os.getenv('DEBUG', False)

    # Data variables.
    CACHE_DIR = os.getenv('CACHE_DIR', './.cache')
    SPREADSHEET_URL = os.getenv('SPREADSHEET_URL', '')

    # Operational variables.
    LOG_NAME = os.getenv('LOG_NAME', 'corji.log')
    LOG_PATH = os.getenv('LOG_PATH', './.logs')

    # Frontend variables.
    GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID', '')
