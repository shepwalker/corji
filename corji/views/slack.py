import json
import logging
import random

from flask import (
    Blueprint,
    render_template,
    request,
    Response
)

from corji.api import CorgiResource
import corji.data_sources.google_spreadsheets as google_spreadsheets
from corji.exceptions import CorgiNotFoundException
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


def generate_slack_failure_case_message(text, image_url=''):
    message = {'text': text}
    if image_url:
        message['attachments'] = [
            {
                'image_url': image_url
            }
        ]
    return json.dumps(message)


def generate_slack_corgi_case(corgi_url):
    message = {
        'response_type': 'in_channel',
        'text': '',
        'attachments': [
            {
                'image_url': corgi_url
            }
        ]
    }
    return json.dumps(message)


@slack_blueprint.route('/slack', methods=['GET', 'POST'])
@logged_view(logger)
def slack_corgi():
    from_name = request.values.get('user_name', '')
    from_team = request.values.get('team_domain', '')
    text = request.values.get('text', '')
    text = text.strip()
    if text_contains_emoji(text):
        emoji = text
        corgis = api.get(emoji)
        if not corgis['count']:
            return generate_slack_failure_case_message(
                'Oh no! No corgi found for emoji {},' +
                ' try sending us a different one!'.format(emoji)),
            200,
            {'Content-Type': 'application/json;'}

    else:
        return generate_slack_failure_case_message(
            'Oh no! No emoji detected in your message! ' +
            'Try sending us an emoji!'), 200,
        {'Content-Type': 'application/json;'}

    corgi_url = random.choice(corgis['results'])
    return generate_slack_corgi_case(corgi_url), 200,
    {'Content-Type': 'application/json;'}
