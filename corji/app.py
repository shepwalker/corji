# This Python file uses the following encoding: utf-8

import random

from flask import (
    Flask,
    render_template,
    request,
)
import twilio.twiml

# Why yes, this *is* janky as hell.  Needed to avoid circular imports.
app = Flask(__name__)

from corji.api import CorgiResource
from corji.data_sources import (
    google_spreadsheets
)
from corji.logging import Logger, logged_view
import corji.settings as settings
from corji.utils import (
    emojis_for_emoticons,
    text_contains_emoji
)

app.config.from_object('corji.settings.Config')

api = CorgiResource()
logger = Logger(app.logger_name,
                settings.Config.LOG_PATH,
                settings.Config.LOG_NAME)


def create_response(text, image_url=None):
    """Crafts a TwiML response using the supplied text and image."""
    resp = twilio.twiml.Response()
    with resp.message(text) as m:
        if image_url:
            m.media(image_url)

    return str(resp)


@app.route("/sms/<original_emoji>", methods=['GET'])
@logged_view(logger)
def get_corgi(original_emoji):
    """Returns the TWIML to mock a given request."""

    message = ""
    emoji = original_emoji

    corgi_urls = api.get(emoji=emoji)["results"]

    # If it's a multi-emoji that we don't track, just grab the first emoji.
    if len(emoji) > 1 and not corgi_urls:
        emoji = original_emoji[0]
        message = render_template('txt/requested_emoji_does_not_exist.txt',
                                  requested_emoji=original_emoji,
                                  fallback_emoji=emoji)
        corgi_urls = api.get(emoji=emoji)["results"]

    # If that still doesn't work, we'll just grab a random one.
    if not corgi_urls:
        logger.warn("Couldn't find corji for {} to remote URL. Using random one.".format(
                    emoji))
        possible_emojis = google_spreadsheets.keys()
        emoji = random.choice(possible_emojis)
        message = render_template('txt/requested_emoji_does_not_exist.txt',
                                  requested_emoji=original_emoji,
                                  fallback_emoji=emoji)
        corgi_urls = api.get(emoji=emoji)["results"]

    # TODO: more sophisticated mechanism of choosing from multiple images.
    corgi_url = random.choice(corgi_urls)

    return create_response(message, image_url=corgi_url)


@app.route("/sms", methods=['GET', 'POST'])
@logged_view(logger)
def corgi():
    """Respond to incoming calls with a simple text message."""
    text = request.values.get("Body") or ""

    if text_contains_emoji(text):
        return get_corgi(text)

    emoji = emojis_for_emoticons.get(text, None)
    if emoji:
        return get_corgi(emoji)

    message = render_template('txt/request_does_not_contain_emoji.txt')
    return create_response(message)


@app.route("/sms/fallback", methods=['GET', 'POST'])
def fallback():
    """Fallback to be called when something else errors."""
    message = render_template('txt/request_failed_fallback.txt')
    return create_response(message, image_url=settings.Config.FALLBACK_IMAGE)


@app.route("/", methods=['GET'])
def about():
    """Much hype.  Very disruptive.  Such blurb."""
    return render_template('html/about.html',
                           google_analytics_id=settings.Config.GOOGLE_ANALYTICS_ID)
