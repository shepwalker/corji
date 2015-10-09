# This Python file uses the following encoding: utf-8

import random

from flask import (
    Flask,
    send_from_directory,
    url_for,
    request
)
import twilio.twiml

# Why yes, this *is* janky as hell.  Needed to avoid circular imports.
app = Flask(__name__)

import corji.cache as cache
import corji.data_sources as data_sources
from corji.exceptions import CorgiNotFoundException
from corji.logging import Logger, logged_view
import corji.settings as settings
from corji.utils import (
    emojis_for_emoticons,
    text_contains_emoji
)

logger = None
app.config.from_object('corji.settings.Config')

logger = Logger(app.logger_name,
                settings.Config.LOG_PATH,
                settings.Config.LOG_NAME)
SPREADSHEET_URL = settings.Config.SPREADSHEET_URL
logger.debug("START: Spreadsheet URL defined: %s", SPREADSHEET_URL)
# TODO: GLOBALS BAD.

corgis = data_sources.load_from_spreadsheet(SPREADSHEET_URL)


# TODO: Serve statics not via Flask.
@app.route("/local/<path:file_name>", methods=['GET'])
def get_image(file_name):
    """Return an emoji image given a file path"""
    file_path = file_name.split('/')
    logger.debug("Attempting to load image from %s", file_name)
    directory = "/".join(file_path[:-1])
    name = file_path[-1]
    logger.debug(
        "Returning image with directory: %s and name: %s", directory, name)
    return send_from_directory(directory, name)


@app.route("/emoji/<original_emoji>", methods=['GET'])
@logged_view(logger)
def get_corgi(original_emoji):
    """Returns the TWIML to mock a given request."""

    message = ""
    emoji = original_emoji
    # If it's a multi-emoji that we don't track, just grab the first emoji.
    if len(emoji) > 1 and emoji not in corgis.keys():
        emoji = original_emoji[0]
        template_name = "corji/templates/requested_emoji_does_not_exist.txt"
        message_template = open(template_name).read()
        message = message_template.format(requested_emoji=original_emoji,
                                          fallback_emoji=emoji)

    # TODO: Use cache, test cache URL, and then fall back.
    try:

        if settings.Config.REMOTE_CACHE_RETRIEVE:
            possible_corji_path = cache.get_from_remote_cache(emoji)
        else:
            possible_corji_path = corgis[emoji]

        if not possible_corji_path:
            raise CorgiNotFoundException()

    except CorgiNotFoundException as e:
        logger.error(e)
        logger.warn("Corji not found for request %s", emoji)
        logger.info("Attempting fallback to remote URL.")

        try:
            possible_corji_path = corgis[emoji]
            if not possible_corji_path:
                raise CorgiNotFoundException()
        except CorgiNotFoundException as e:
            # Add a random emoji instead of just a sadface.
            possible_emojis = [e for e in corgis.keys() if corgis[e]]
            random_emoji = random.choice(possible_emojis)
            template_name = "corji/templates/requested_emoji_does_not_exist.txt"
            message_template = open(template_name).read()
            message = message_template.format(requested_emoji=original_emoji,
                                              fallback_emoji=random_emoji)
            if settings.Config.REMOTE_CACHE_RETRIEVE:
                possible_corji_path = cache.get_from_remote_cache(random_emoji)
            else:
                possible_corji_path = corgis[random_emoji]

    # Only append base URL if it's a local path.
    if "http" not in possible_corji_path:
        # Remove the trailing slash since we're appending a relative URL.
        base_url = request.url_root[:-1]

        image_path = url_for('get_image', file_name=possible_corji_path)
        absolute_image_url = base_url + image_path
    else:
        absolute_image_url = possible_corji_path

    resp = twilio.twiml.Response()
    with resp.message(message) as m:
        m.media(absolute_image_url)

    return str(resp)


@app.route("/", methods=['GET', 'POST'])
@logged_view(logger)
def corgi():
    """Respond to incoming calls with a simple text message."""
    text = request.values.get("Body") or ""

    if text_contains_emoji(text):
        return get_corgi(text)

    emoji = emojis_for_emoticons.get(text, None)
    if emoji:
        return get_corgi(emoji)

    template_name = "corji/templates/request_does_not_contain_emoji.txt"
    no_emoji_message = open(template_name, encoding='utf-8').read()
    resp = twilio.twiml.Response()
    resp.message(no_emoji_message)
    return str(resp)
