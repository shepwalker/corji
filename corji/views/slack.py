import json
import logging
import random

from flask import (
    Blueprint,
    render_template,
    request
)

from corji.api import CorgiResource
import corji.data_sources.google_spreadsheets as google_spreadsheets
from corji.logging import logged_view
import corji.settings as settings
from corji.utils.emoji import (
    text_contains_emoji,
    emojis_for_emoticons,
    emoji_contains_skin_tone,
    emoji_is_numeric
)

slack_blueprint = Blueprint('slack', __name__,
                            template_folder='templates')

api = CorgiResource()

logger = logging.getLogger(settings.Config.LOGGER_NAME)


def generate_slack_failure_case_message(text, image_url=""):
    message = {}
    message['text'] = text
    if image_url:
        attachment = {}
        attachment = {'image_url': image_url}
        attachment_array = [attachment]
        message['attachments'] = attachment_array
    return json.dumps(message)


def generate_slack_corgi_case(corgi_url):
    message = {}
    message['response_type'] = "in_channel"
    message['text'] = ""
    attachment = {}
    attachment = {'image_url': corgi_url}
    attachment_array = [attachment]
    message['attachments'] = attachment_array
    return json.dumps(message)


@slack_blueprint.route("/slack", methods=['GET', 'POST'])
@logged_view(logger)
def slack_corgi():
    from_name = request.values.get("user_name") or ""
    from_team = request.values.get("team_domain") or ""
    text = request.values.get("text") or ""
    text = text.strip()
    if text_contains_emoji(text):
        emoji = text
    else:
        emoji = emojis_for_emoticons.get(text, None)
        if not emoji:
            return generate_slack_failure_case_message("No emoji detected! Try sending us an emoji!")
    # If it's a multi-emoji that we don't track, just grab the first emoji.
    # TODO: abstract out use of `keys()`.
    if len(emoji) > 1 and emoji not in google_spreadsheets.keys():
        emoji = text[0]

        # Check for skin-toned emojis.
        # (This only handles the one-emoji case for now.)
        if not emoji_contains_skin_tone(text) and not emoji_is_numeric(text):
            return generate_slack_failure_case_message("No emoji detected! Try sending us an emoji!")

    # Time to grab the filepath for the emoji!
    corgi_urls = api.get(emoji)['results']

    # If that still doesn't work, we'll just grab a random one.
    if not corgi_urls:
        return generate_slack_failure_case_message("Oh nos! We don't have an corgi for that emoji! Try a different one!")

    corgi_url = random.choice(corgi_urls)

    return generate_slack_corgi_case(corgi_url)
    