from functools import wraps
import logging
import os
import sys
from logging.handlers import (
    TimedRotatingFileHandler
)


"""
LOG LEVELS:
DEBUG being used for service start/regular events
INFO being used for all happy-path requests
WARN being used for happy-path requests that can't find valid corji
ERROR being used for errors (though not actually logging this well yet)
"""

# TODO: Actually make this a class.
def Logger(app, log_path, log_name):
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception as e:
            # TODO: WTF
            pass

    file_handler = TimedRotatingFileHandler(log_path + '/' + log_name, 'midnight', 1)
    file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    file_handler.setLevel(logging.INFO)
    logger = app.logger
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    if app.debug:
        local_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(local_handler)
    return logger

def logged_view(logger):
    def inner_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logger.info("Request: %s", args or "")
            fn = f(*args, **kwargs)
            logger.info("Response: %s", fn)
            return fn
        return decorated_function
    return inner_decorator
