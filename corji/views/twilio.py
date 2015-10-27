"""Views that return TwiML."""

import logging
import random

from flask import (
    Blueprint,
    render_template,
    request,
    url_for
)
import twilio.twiml

from corji.api import CorgiResource
import corji.customer_data as customer_data
import corji.data_sources.google_spreadsheets as google_spreadsheets
from corji.exceptions import (
    UserNotFoundException,
    CorjiFreeLoaderException
)
from corji.logging import logged_view
import corji.settings as settings
from corji.utils.emoji import (
    emojis_for_emoticons,
    emoji_contains_skin_tone,
    emoji_is_numeric,
    text_contains_emoji
)

from corji.utils.message import (
    process_interrupts
)
from corji.utils.twilio import (
    create_response
)

from corji.messages.messages import (
    EmojiRequest,
    create_message
)

from corji.utils.message import (
    process_interrupts
)

twilio_blueprint = Blueprint('twilio', __name__,
                             template_folder='templates')
logger = logging.getLogger(settings.Config.LOGGER_NAME)

api = CorgiResource()


@twilio_blueprint.route("/sms/<original_emoji>", methods=['GET'])
@logged_view(logger)
def get_corgi(original_emoji):
    """Returns the TWIML to mock a given request."""

    message = ""
    emoji = original_emoji

    # If it's a multi-emoji that we don't track, just grab the first emoji.
    # TODO: abstract out use of `keys()`.
    if len(emoji) > 1 and emoji not in google_spreadsheets.keys():
        emoji = original_emoji[0]

        # Check for skin-toned emojis.
        # (This only handles the one-emoji case for now.)
        if not emoji_contains_skin_tone(original_emoji) and not emoji_is_numeric(original_emoji):
            message = render_template('txt/requested_emoji_does_not_exist.txt',
                                      requested_emoji=original_emoji,
                                      fallback_emoji=emoji)

    # Time to grab the filepath for the emoji!
    corgi_urls = api.get(emoji)['results']

    # If that still doesn't work, we'll just grab a random one.
    if not corgi_urls:
        logger.warn("Couldn't find corgi for {}. Using random one.".format(
                    emoji))

        while not corgi_urls:
            results = api.get()
            emoji, corgi_urls = results['emoji'], results['results']
        message = render_template('txt/requested_emoji_does_not_exist.txt',
                                  requested_emoji=original_emoji,
                                  fallback_emoji=emoji)

    corgi_url = random.choice(corgi_urls)
    return create_response(message, image_url=corgi_url)


@twilio_blueprint.route("/sms", methods=['GET', 'POST'])
@logged_view(logger)
def corgi():
    """Respond to incoming calls with a simple text message."""
    phone_number = request.values.get("From") or ""
    text = request.values.get("Body") or ""

    # If the phone number doesn't exist, it's not a real request.
    if not phone_number:
        return ""

    customer = customer_data.get(phone_number) or {}

    # If customer has asked us to stop, we stop.
    if customer.get('stop', None):
        return ""

    if not customer:
        customer = customer_data.new(phone_number)

    # Process any system-wide or user-specific interrupts.
    interrupts = process_interrupts(customer)

    # Tricky because we want to return an empty string if it appears.
    if interrupts is not None:
        return interrupts

    # generate instance of Abstract Message that
    # corresponds ot input
    message = create_message(text, phone_number)

    try:
        return message.create_reply()
    except CorjiFreeLoaderException:
        return generate_freeloader_response(customer)

    # If they tell us to stop, then stop.
    if "stop" in text.lower():
        customer_data.add_metadata(phone_number, 'stop', 'true')
        message = render_template('txt/request_asks_to_stop.txt')
        return create_response(message)

    # Fallback case: no emojis, just text.
    message = render_template('txt/request_does_not_contain_emoji.txt')
    return create_response(message)


@twilio_blueprint.route("/sms/fallback", methods=['GET', 'POST'])
def fallback():
    """Fallback to be called when something else errors."""
    message = render_template('txt/request_failed_fallback.txt')
    return create_response(message, image_url=settings.Config.FALLBACK_IMAGE)


@twilio_blueprint.route("/voice", methods=['GET', 'POST'])
def voice():
    """Corgis don't know how to use the phone!"""
    message = render_template('txt/request_is_via_voice.txt')
    resp = twilio.twiml.Response()
    resp.say(message)
    return str(resp)
