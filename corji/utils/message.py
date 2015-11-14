"""
Set of utility functions for processing messages
and replying.
"""
from functools import wraps

from flask import (
    render_template,
    url_for
)

from corji.models import emoji_customer
from corji.exceptions import CorjiFreeloaderException, UserNotFoundException
import corji.settings as settings
from corji.utils.twilio import create_response


def consumed_func():
    """
    Decorator that decrements consumption "credit" for a User after
    successful execution of the wrapped function.
    Throws error if user is out of consumption credits.
    """
    def inner_decorator(f):
        @wraps(f)
        def decorated_function(self, *args):
            customer = emoji_customer.get(self.phone_number) or {}
            if not customer:
                raise UserNotFoundException
            if int(customer['consumptions']['N']) < 1 and not customer.get('override', None):
                raise CorjiFreeloaderException
            fn = f(self, *args)
            if fn:
                emoji_customer.modify_consumptions(self.phone_number, 1)
            return fn
        return decorated_function
    return inner_decorator


def process_interrupts(customer, text):
    """
    Processes user input for global, or user-specific process_interrupts
    that would preclude sending a message to the user.
    NONE should be treated as no relevant interrupts, so messaging can proceed
    empty string should be treated as a no-response to the user
    """
    if customer and customer.get('stop', None):
        return ""

    if settings.Config.DO_NOT_DISTURB and customer and not customer.get('override', None):
        phone_number = customer['phone_number'].get('S', '')

        if "corgi" in text.lower() and not customer.get('wants_uptime_notification', None):
            message = render_template('txt/do_not_disturb_acknowledged.txt')
            emoji_customer.add_metadata(phone_number, 'wants_uptime_notification', 'true')
            return create_response(message)

        if customer.get('showed_disable_prompt', None):
            return ""

        emoji_customer.add_metadata(phone_number, 'showed_disable_prompt', 'true')
        message = render_template('txt/do_not_disturb.txt')
        return create_response(message)

    return None


def generate_freeloader_response(customer):
    if customer.get('showed_payment_prompt', None):
        return ""
    emoji_customer.add_metadata(phone_number, 'showed_payment_prompt', 'true')
    message = render_template('txt/pay_us_please.txt',
                              site_url=settings.Config.SITE_URL,
                              payment_url=url_for('request_charge'),
                              phone_number=phone_number)
    return create_response(message)
