# This Python file uses the following encoding: utf-8

from functools import wraps
import logging
import os
import sys
from logging.handlers import (
    TimedRotatingFileHandler
)

from slack_log_handler import SlackLogHandler

from corji.settings import Config

"""
LOG LEVELS:
DEBUG being used for service start/regular events
INFO being used for all happy-path requests
WARN being used for happy-path requests that can't find valid corji
ERROR being used for errors (though not actually logging this well yet)
"""


# TODO: Actually make this a class.
def Logger(logger_name, log_path, log_name):
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            # TODO: WTF
            pass
    # Get logger, set debug level
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Setup file handler log rotating by day
    qualified_log_name = log_path + '/' + log_name
    file_handler = TimedRotatingFileHandler(qualified_log_name, 'midnight', 1)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s %(filename)s %(funcName)s %(lineno)d'))
    file_handler.setLevel(logging.DEBUG)

    # Setup local handler to output to stderr
    local_handler = logging.StreamHandler(sys.stderr)

    # Build/add slack handler
    if Config.SLACK_ERROR_LOGGING_ENABLED:
        slack_handler = SlackLogHandler(Config.SLACK_LOG_WEBHOOK_URL)
        slack_handler.setLevel(logging.ERROR)
        logger.addHandler(slack_handler)
        
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(local_handler)

    return logger


def logged_view(logger):
    def inner_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if logger:
                logger.info("Request: %s", args or "")
            fn = f(*args, **kwargs)
            if logger:
                logger.info("Response: %s", fn)
            return fn
        return decorated_function
    return inner_decorator
