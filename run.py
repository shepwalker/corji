# This Python file uses the following encoding: utf-8

from logging.handlers import (
    TimedRotatingFileHandler
)
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
from log import Logger, logged_view
import settings

app = Flask(__name__)
app.config.from_object('settings.Config')

LOG_PATH = app.config['CORJI_LOG_PATH']
LOG_NAME = app.config['CORJI_LOG_NAME']
logger = Logger(Flask(__name__), LOG_PATH, LOG_NAME)

SPREADSHEET_URL = app.config['CORJI_SPREADSHEET_URL']
logger.debug("START: Spreadsheet URL defined: %s", SPREADSHEET_URL)
# TODO: GLOBALS BAD.
corgis = data_sources.load_from_spreadsheet(SPREADSHEET_URL)

logger.debug("START: Starting to load Corjis into cache.")
cache.put_in_local_cache(corgis)
logger.debug("START: Completed Corji Cache loading")


# TODO: Serve statics not via Flask.
@app.route("/local/<path:file_name>", methods=['GET'])
def get_image(file_name):
    """Return an emoji image given a file path"""
    file_path = file_name.split('/')
    directory = "/".join(file_path[:-1])
    name = file_path[-1]
    return send_from_directory(directory, name)


@app.route("/emoji/<emoji>", methods=['GET'])
def get_corgi(emoji):
    """Returns the TWIML to mock a given request."""

    resp = twilio.twiml.Response()

    try:
        possible_corji_path = cache.get_from_local_cache(emoji)
    except CorgiNotFoundException as e:
        logger.warn("Corji not found for request %s", emoji)
        return str(resp.message(e.message()))

    # Remove the trailing slash since we're appending a relative URL.
    base_url = request.url_root[:-1]

    image_path = url_for('get_image', file_name=possible_corji_path)
    absolute_image_url = base_url + image_path

    with resp.message() as m:
        m.media(absolute_image_url)

    return str(resp)


@app.route("/", methods=['GET', 'POST'])
@logged_view(logger)
def corgi():
    """Respond to incoming calls with a simple text message."""
    this_emoji = request.values.get("Body") or ""
    return get_corgi(this_emoji)

if __name__ == "__main__":
    app.run(debug=True)
