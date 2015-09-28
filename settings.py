import os

class Config(object):
	CACHE_DIR = os.getenv('CACHE_DIR', './.cache')
	DEBUG = os.getenv('DEBUG', False)
	LOG_NAME = os.getenv('LOG_NAME', 'corji.log')
	LOG_PATH = os.getenv('LOG_PATH', './.logs')
	SPREADSHEET_URL = os.getenv('SPREADSHEET_URL', '')
