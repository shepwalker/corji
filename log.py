from functools import wraps
import logging
import os
import sys

"""LOG LEVELS:
DEBUG being used for service start/regular events
INFO being used for all happy-path requests
WARN being used for happy-path requests that can't find valid corji
ERROR being used for errors (though not actually logging this well yet)
"""
from logging.handlers import (
    TimedRotatingFileHandler
)

main_logger = ""

def setup_app_logger(app):
	if not os.path.exists(app.config['CORJI_LOG_PATH']):
		os.makedirs(app.config['CORJI_LOG_PATH'])
	global main_logger
	file_handler = TimedRotatingFileHandler(app.config['CORJI_LOG_PATH'] + '/' + app.config['CORJI_LOG_NAME'], 'midnight', 1)
	file_handler.setFormatter(
	logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
	file_handler.setLevel(logging.INFO)
	main_logger = app.logger
	main_logger.addHandler(file_handler)
	main_logger.setLevel(logging.INFO)
	if app.debug:
	    local_handler = logging.StreamHandler(sys.stdout)
	    main_logger.addHandler(local_handler)
	return main_logger

def logged_view(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
	    main_logger.info("REQUEST: Request to Corji: %s", "" if args is None else args)
	    fn = f(*args, **kwargs)
	    main_logger.info("REQUEST: Response to Corji: %s", fn)
	    return fn
	return decorated_function