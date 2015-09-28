import os

class Config(object):
	DEBUG = os.getenv('DEBUG', False)
	CORJI_LOG_PATH = os.getenv('CORJI_LOG_PATH', './logs')
	CORJI_LOG_NAME = os.getenv('CORJI_LOG_NAME', 'corji.log')
	CORJI_SPREADSHEET_URL = os.getenv('CORGI_URL', '')
