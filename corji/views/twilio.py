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
from corji.logging import logged_view
import corji.settings as settings
from corji.utils.emoji import (
    emojis_for_emoticons,
    emoji_contains_skin_tone,
    emoji_is_numeric,
    text_contains_emoji
)

twilio_blueprint = Blueprint('twilio', __name__,
                             template_folder='templates')
logger = logging.getLogger(settings.Config.LOGGER_NAME)

api = CorgiResource()


def create_response(text, image_url=None):
    """Crafts a TwiML response using the supplied text and image."""
    resp = twilio.twiml.Response()
    with resp.message(text) as m:
        if image_url:
            m.media(image_url)

    return str(resp)


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

    if settings.Config.DO_NOT_DISTURB and not customer.get('override', None):
        if customer.get('showed_disable_prompt', None):
            return ""

        customer_data.add_metadata(phone_number, 'showed_disable_prompt', 'true')
        message = render_template('txt/do_not_disturb.txt')
        return create_response(message)

    # TODO: test this shit, ffs.
    if not customer:
        customer_data.new(phone_number)
    elif int(customer['consumptions']['N']) < 1 and not(customer.get('override', None)):
        if customer.get('showed_payment_prompt', None):
            return ""
        customer_data.add_metadata(phone_number, 'showed_payment_prompt', 'true')
        message = render_template('txt/pay_us_please.txt',
                                  site_url=settings.Config.SITE_URL,
                                  payment_url=url_for('request_charge'),
                                  phone_number=phone_number)
        return create_response(message)
    else:
        customer_data.modify_consumptions(phone_number, -1)

    # Let's just ignore trailing whitespace.
    text = text.strip()

    # Base case: the text has emoji.
    if text_contains_emoji(text):
        return get_corgi(text)

    # Edge case: the text has emoticons but not emoji.
    emoji = emojis_for_emoticons.get(text, None)
    if emoji:
        return get_corgi(emoji)

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
