"""Views that return TwiML."""
import logging

from flask import (
    Blueprint,
    redirect,
    render_template,
    request
)
import twilio.twiml

from corji.api import CorgiResource
import corji.customer_data as customer_data
from corji.exceptions import (
    CorjiFreeloaderException
)
from corji.logging import logged_view
import corji.settings as settings
from corji.utils.message import (
    process_interrupts
)
from corji.utils.twilio import (
    create_response
)
from corji.messages.messages import (
    create_message
)

twilio_blueprint = Blueprint('twilio', __name__,
                             template_folder='templates')
logger = logging.getLogger(settings.Config.LOGGER_NAME)

api = CorgiResource()


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
    interrupts = process_interrupts(customer, text)

    # Tricky because we want to return an empty string if it appears.
    if interrupts is not None:
        return interrupts

    # generate instance of Abstract Message that
    # corresponds to input
    message = create_message(text, phone_number)

    if not message:
        message = render_template('txt/request_does_not_contain_emoji.txt')
        return create_response(message)
    try:
        return message.create_reply()
    except CorjiFreeloaderException:
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
    