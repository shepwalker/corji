"""Random, likely static, views that don't actually consist within the app."""
import random

from celery import Celery
from flask import (
    Blueprint,
    request,
    render_template
)
from twilio.rest import TwilioRestClient

from corji.api import CorgiResource
from corji.data_sources import (
    google_spreadsheets
)
from corji.settings import Config

celery = Celery("corji", broker=Config.CELERY_BROKER_URL)
marketing_blueprint = Blueprint('marketing', __name__,
                                template_folder='templates')


@marketing_blueprint.route("/", methods=['GET'])
def about():
    """Much hype.  Very disruptive.  Such blurb."""
    return render_template('html/marketing/about.html',
                           google_analytics_id=Config.GOOGLE_ANALYTICS_ID)


@marketing_blueprint.route("/pile", methods=['GET'])
def piledrive():
    target = request.values.get("Target", "8046989478")
    count = int(request.values.get("Count", "3"))
    print(target)
    pile.delay(target, count)
    return ":)"


@celery.task
def pile(target, count):
    """Much hype.  Very disruptive.  Such blurb."""

    api = CorgiResource()
    client = TwilioRestClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

    number_of_corgis_to_send = count
    corgis = []

    while len(corgis) < number_of_corgis_to_send:
        random_emoji = random.choice(google_spreadsheets.keys())
        results = api.get(random_emoji)['results']
        if len(results):
            for result in results:
                if result not in corgis:
                    corgis.append(result)

    for corgi in corgis:
        message = client.messages.create(
            media_url=corgi,
            to=target,
            from_=Config.TWILIO_PHONE_NUMBER
        )
