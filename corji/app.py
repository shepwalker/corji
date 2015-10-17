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

import corji.customer_data as customer_data
from corji.data_sources import (
    google_spreadsheets,
    s3
)
from corji.exceptions import CorgiNotFoundException
from corji.logging import Logger, logged_view
import corji.settings as settings
from corji.utils import (
    emojis_for_emoticons,
    emoji_contains_skin_tone,
    text_contains_emoji
)

app.config.from_object('corji.settings.Config')

logger = Logger(app.logger_name,
                settings.Config.LOG_PATH,
                settings.Config.LOG_NAME)

google_spreadsheets.load(settings.Config.SPREADSHEET_URL)

if settings.Config.REMOTE_CACHE_RETRIEVE:
    s3.load()


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

    # If it's a multi-emoji that we don't track, just grab the first emoji.
    if len(emoji) > 1 and emoji not in google_spreadsheets.keys():
        emoji = original_emoji[0]

        # Check for skin-toned emojis.
        # (This only handles the one-emoji case for now.)
        if not emoji_contains_skin_tone(original_emoji):
            message = render_template('txt/requested_emoji_does_not_exist.txt',
                                      requested_emoji=original_emoji,
                                      fallback_emoji=emoji)

    # Time to grab the filepath for the emoji!
    possible_corji_path = None

    # First we'll try using S3.
    if settings.Config.REMOTE_CACHE_RETRIEVE:
        try:
            possible_corji_path = s3.get(emoji)
        except CorgiNotFoundException as e:
            logger.error(e)
            logger.warn("Corji not found for emoji %s", emoji)

    # Then we'll try using the external copy.
    if not possible_corji_path:
        possible_corji_path = google_spreadsheets.get(emoji)

    # If that still doesn't work, we'll just grab a random one.
    if not possible_corji_path:
        logger.warn("Couldn't find corji for {} to remote URL. Using random one.".format(
                    emoji))
        possible_emojis = google_spreadsheets.keys()
        emoji = random.choice(possible_emojis)
        message = render_template('txt/requested_emoji_does_not_exist.txt',
                                  requested_emoji=original_emoji,
                                  fallback_emoji=emoji)
        possible_corji_path = google_spreadsheets.get(emoji)

    return create_response(message, image_url=possible_corji_path)


@app.route("/sms", methods=['GET', 'POST'])
@logged_view(logger)
def corgi():
    """Respond to incoming calls with a simple text message."""
    phone_number = request.values.get("From") or ""
    text = request.values.get("Body") or ""

    # Keep track of phone numbers.
    customer = customer_data.get(phone_number)
    if not customer:
        customer_data.new(phone_number)
    else:
        customer_data.increment_consumptions(phone_number)

    # Let's just ignore trailing whitespace.
    text = text.strip()

    if text_contains_emoji(text):
        return get_corgi(text)

    emoji = emojis_for_emoticons.get(text, None)
    if emoji:
        return get_corgi(emoji)

    message = render_template('txt/request_does_not_contain_emoji.txt')
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)


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
