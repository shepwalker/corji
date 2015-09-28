# This Python file uses the following encoding: utf-8

import random

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
from utils import text_contains_emoji

app = Flask(__name__)
app.config.from_object('settings.Config')

logger = Logger(Flask(__name__),
                app.config['CORJI_LOG_PATH'],
                app.config['CORJI_LOG_NAME'])

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

    message = ""
    try:
        possible_corji_path = cache.get_from_local_cache(emoji)
    except CorgiNotFoundException as e:
        logger.error(e)
        logger.warn("Corji not found for request %s", emoji)

        # Add a random emoji instead fo just a sadface.
        possible_emojis = [emoji for emoji in corgis.keys() if corgis[emoji]]
        random_emoji = random.choice(possible_emojis)
        message_template = open("templates/requested_emoji_does_not_exist.txt").read()
        message = message_template.format(requested_emoji = emoji,
                                          fallback_emoji = random_emoji)
        possible_corji_path = cache.get_from_local_cache(random_emoji)


    # Remove the trailing slash since we're appending a relative URL.
    base_url = request.url_root[:-1]

    image_path = url_for('get_image', file_name=possible_corji_path)
    absolute_image_url = base_url + image_path

    with resp.message(message) as m:
        m.media(absolute_image_url)

    return str(resp)


@app.route("/", methods=['GET', 'POST'])
@logged_view(logger)
def corgi():
    """Respond to incoming calls with a simple text message."""
    text = request.values.get("Body") or ""
    if not text_contains_emoji(text):
        no_emoji_message = open("templates/request_does_not_contain_emoji.txt").read()
        resp = twilio.twiml.Response()
        return str(resp.message(no_emoji_message))
    return get_corgi(text)

if __name__ == "__main__":
    app.run(debug=True)
