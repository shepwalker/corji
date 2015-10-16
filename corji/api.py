import logging

from flask_restful import Resource, Api

from corji.data_sources import (
    google_spreadsheets,
    s3
)
from corji.exceptions import CorgiNotFoundException
import corji.settings as settings
from corji.utils import (
    emoji_contains_skin_tone
)

logger = logging.getLogger(settings.Config.LOGGER_NAME)
google_spreadsheets.load(settings.Config.SPREADSHEET_URL)
s3.load()


class CorgiResource(Resource):
    def get(self, emoji):

        # The string we eventually return.
        corgi_url = ""

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

        return {
            "count": len(corgi_url),
            "results": corgi_urls
        }


def attach_rest_api(app):
    api = Api(app)
    api.add_resource(CorgiResource, '/rest/<string:emoji>')
