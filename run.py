# This Python file uses the following encoding: utf-8
import logging
import os

from logging.handlers import (
    TimedRotatingFileHandler
)
from functools import wraps
from flask import (
    Flask,
    send_from_directory,
    url_for,
    request
)
import twilio.twiml

import cache
import data_sources
from exceptions import CorgiNotFoundException
from log import setup_app_logger
import settings

app = Flask(__name__)
app.config.from_object('settings.Config')
# logging nonsense
logpath = app.config['CORJI_LOG_PATH']
logname = app.config['CORJI_LOG_NAME']

mainLogger = setup_app_logger(app)

SPREADSHEET_URL = app.config['CORJI_SPREADSHEET_URL']
mainLogger.debug("START: Spreadsheet URL defined: %s", SPREADSHEET_URL)
# TODO: GLOBALS BAD.
corgis = data_sources.load_from_spreadsheet(SPREADSHEET_URL)

mainLogger.debug("START: Starting to load Corjis into cache.")
cache.put_in_local_cache(corgis)
mainLogger.debug("START: Completed Corji Cache loading")


def logged_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        mainLogger.info("REQUEST: Request to Corji: %s",args)
        fn = f(*args, **kwargs)
        mainLogger.info("REQUEST: Response to Corji: %s", fn)
        return fn
    return decorated_function

# TODO: Serve statics not via Flask.
@app.route("/local/<path:file_name>", methods=['GET'])
def get_image(file_name):
    """Return an emoji image given a file path"""
    file_path = file_name.split('/')
    directory = "/".join(file_path[:-1])
    name = file_path[-1]
    return send_from_directory(directory, name)


@app.route("/mock/<emoji>", methods=['GET'])
def get_corgi(emoji):
    """Returns the TWIML to mock a given request."""

    resp = twilio.twiml.Response()

    try:
        possible_corji_path = cache.get_from_local_cache(emoji)
    except CorgiNotFoundException as e:
        mainLogger.warn("Corji not found for request %s", emoji)
        return str(resp.message(e.message()))

    corgi = request.url_root + \
        url_for('get_image', file_name=possible_corji_path)
    with resp.message() as m:
        m.media(corgi)

    return str(resp)


@app.route("/", methods=['GET', 'POST'])
@logged_view
def corgi():
    """Respond to incoming calls with a simple text message."""
    this_emoji = request.values.get("Body") or ""
    return get_corgi(this_emoji)

if __name__ == "__main__":
    app.run(debug=True)
