import logging
import random

from flask_restful import Resource, Api
import requests

from corji.data_sources import (
    google_spreadsheets,
    s3
)
from corji.exceptions import CorgiNotFoundException
import corji.settings as settings
from corji.utils.emoji import (
    emoji_contains_skin_tone,
    text_contains_emoji
)

logger = logging.getLogger(settings.Config.LOGGER_NAME)
google_spreadsheets.load(settings.Config.SPREADSHEET_URL)
if settings.Config.REMOTE_CACHE_RETRIEVE:
    s3.load()


class CorgiResource(Resource):
    def get(self, emoji=None):
        """Returns an emoji associated with the given emoji.
        If no emoji is supplied, a random corji is returned."""

        if not emoji:
            emoji = random.choice(google_spreadsheets.keys())

        # Check for skin-toned emojis and fallback to the undecorated one.
        if len(emoji) == 2 and emoji_contains_skin_tone(emoji):
            emoji = emoji[0]

        # First we'll try using S3.
        if settings.Config.REMOTE_CACHE_RETRIEVE:
            try:
                corgi_urls = s3.get_all(emoji)
            except CorgiNotFoundException as e:
                logger.error(e)
                logger.warn("Corji not found for emoji %s", emoji)

        # If S3 is a no-go, fall back to Spreadsheets.
        corgi_urls = google_spreadsheets.get_all(emoji)

        # TODO: do this smarter somehow.
        for url in corgi_urls:
            try:
                requests.get(url)
            except Exception as e:
                logger.warn("URL {} is invalid; not returning.".format(url))
                corgi_urls.remove(url)

        return {
            "count": len(corgi_urls),
            "emoji": emoji if text_contains_emoji(emoji) else "",
            "results": corgi_urls
        }


def attach_rest_api(app):
    api = Api(app)
    api.add_resource(CorgiResource, '/rest/<string:emoji>')
