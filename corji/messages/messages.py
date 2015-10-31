import logging
import random

from flask import render_template

from corji.api import CorgiResource
import corji.data_sources.google_spreadsheets as google_spreadsheets
import corji.settings as settings
from corji.utils.emoji import (
    text_contains_emoji,
    emojis_for_emoticons,
    emoji_contains_skin_tone,
    emoji_is_numeric
)
from corji.utils.message import (
    consumed_func
)
from corji.utils.twilio import (
    create_response
)

api = CorgiResource()

logger = logging.getLogger(settings.Config.LOGGER_NAME)


def create_message(text, phone_number):
    if emojis_for_emoticons.get(text, None) or text_contains_emoji(text):
        return EmojiRequest(text, phone_number)

    return None


class AbstractCorjiRequest(object):
    """Abstract class for messages received to the service"""

    def __init__(self, text, phone_number):
        self.text = text
        self.phone_number = phone_number

    def create_reply(self):
        raise NotImplementedError


class EmojiRequest(AbstractCorjiRequest):
    """Request class for messages that contain emoji or emoticons"""

    @consumed_func()
    def create_reply(self):
        message = ""
        text = self.text
        text = text.strip()
        if text_contains_emoji(text):
            emoji = text
        else:
            emoji = emojis_for_emoticons.get(text, None)
            if not emoji:
                raise RuntimeError("Improperly identified message type")
        # If it's a multi-emoji that we don't track, just grab the first emoji.
        # TODO: abstract out use of `keys()`.
        if len(emoji) > 1 and emoji not in google_spreadsheets.keys():
            emoji = text[0]

            # Check for skin-toned emojis.
            # (This only handles the one-emoji case for now.)
            if not emoji_contains_skin_tone(text) and not emoji_is_numeric(text):
                message = render_template('txt/requested_emoji_does_not_exist.txt',
                                          requested_emoji=text,
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
                                      requested_emoji=text,
                                      fallback_emoji=emoji)

        corgi_url = random.choice(corgi_urls)
        return create_response(message, image_url=corgi_url)


class SecretRequest(AbstractCorjiRequest):
    def create_reply(self):
        raise NotImplementedError
