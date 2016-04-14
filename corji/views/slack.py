import json
import logging
import random

from emoji import emojize
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    Response,
    url_for
)
import requests

from corji.api import CorgiResource
import corji.data_sources.google_spreadsheets as google_spreadsheets
from corji.exceptions import CorgiNotFoundException
from corji.logging import logged_view
from corji.models import slack_customer
from corji.settings import Config
from corji.utils.emoji import (
    text_contains_emoji,
    emojis_for_emoticons,
    emoji_contains_skin_tone,
    emoji_is_numeric
)

slack_blueprint = Blueprint('slack', __name__,
                            template_folder='templates')

api = CorgiResource()

logger = logging.getLogger(Config.LOGGER_NAME)


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
                'text': '',
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
    corgis = {}
    if text_contains_emoji(text):
        emoji = text
        corgis = api.get(emoji)
        if not corgis['count']:
            response_content = generate_slack_failure_case_message(
                'Oh no! No corgi found for emoji {},' +
                ' try sending us a different one!'.format(emoji)),
            return Response(response_content, mimetype='application/json')
    else:
        detected_emoji = emojize(text, use_aliases=True)
        if len(detected_emoji) != len(text):
            corgis = api.get(detected_emoji)
    if not corgis or not corgis['count']:
        response_content = generate_slack_failure_case_message(
            'Oh no! No emoji detected in your message! ' +
            'Try sending us an emoji!')
        return Response(response_content, mimetype='application/json')

    corgi_url = random.choice(corgis['results'])
    response_content = generate_slack_corgi_case(corgi_url)
    return Response(response_content, mimetype='application/json')


@slack_blueprint.route("/slack/about", methods=['GET'])
def about_slack():
    code = request.args.get('code', '')
    redirect_uri = url_for("slack.about_slack", _external=True)
    if code:
        try:
            auth_response = requests.post('https://slack.com/api/oauth.access',
                                  data={
                                      'client_id': Config.SLACK_ID,
                                      'client_secret': Config.SLACK_SECRET,
                                      'code': code,
                                      'redirect_uri':"asdfasdfasdfsd"
                                  })
            response_content = json.loads(auth_response.text)
            if response_content and response_content['ok']:
                slack_customer.new(
                    response_content['team_id'],
                    response_content['access_token'],
                    response_content['team_name']
                )
        except:
            logger.error("error on processing logger auth attempt")
            logger.error(auth_response.text)
    # TODO: PRESENT ERROR IN ABOUT PAGE IF THIS ERRORS OUT

    return render_template('html/marketing/slack_about.html',
                           google_analytics_id=Config.GOOGLE_ANALYTICS_ID,
                           slack_redirect_uri=redirect_uri)
