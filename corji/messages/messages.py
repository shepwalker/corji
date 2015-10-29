import random

from corji.api import CorgiResource
from corji.utils.emoji import (
    text_contains_emoji,
    emojis_for_emoticons
    )
from corji.utils.message import consumed_func

api = CorgiResource()

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

    @consumed_func()
    def create_reply(self):
        text = self.text
        text = text.strip()
        if text_contains_emoji(text):
            results = api.get(text)

        # Edge case: the text has emoticons but not emoji.
        emoji = emojis_for_emoticons.get(text, None)
        if emoji:
            results = api.get(emoji)
        if results:
            emoji, corgi_urls = results['emoji'], results['results']
            return random.choice(corgi_urls)
        raise RuntimeError("Improperly identified message type")
        return None
    
class SecretRequest(AbstractCorjiRequest):
    """docstring for ClassName"""
    def __init__(self, body, sender):
        super(ClassName, self).__init__(body, sender)
        self.arg = arg

    
    def create_reply(self):
        text = self.body
        text = text.strip()
        return get_corgi(text)
