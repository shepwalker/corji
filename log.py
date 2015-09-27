import logging
import os
import sys
#LOG LEVELS:
#DEBUG being used for service start/regular events
#INFO being used for all happy-path requests
#WARN being used for happy-path requests that can't find valid corji
#ERROR being used for errors (though not actually logging this well yet)
from logging.handlers import (
    TimedRotatingFileHandler
)

def setup_app_logger(app):
	if not os.path.exists(app.config['CORJI_LOG_PATH']):
		os.makedirs(app.config['CORJI_LOG_PATH'])
	file_handler = TimedRotatingFileHandler(app.config['CORJI_LOG_PATH'] + '/' + app.config['CORJI_LOG_NAME'], 'midnight', 1)
	file_handler.setFormatter(
	logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
	file_handler.setLevel(logging.INFO)
	mainLogger = app.logger
	mainLogger.addHandler(file_handler)
	mainLogger.setLevel(logging.INFO)
	if app.debug:
	    local_handler = logging.StreamHandler(sys.stdout)
	    mainLogger.addHandler(local_handler)
	return mainLogger