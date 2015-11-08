"""Random, likely static, views that don't actually consist within the app."""
import random

from celery import Celery
from flask import (
    Blueprint,
    request,
    render_template
)
import stripe
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


@marketing_blueprint.route("/pile", methods=['POST'])
def piledrive():
    recipient_number = request.form['target']
    sender_name = request.form['name']

    email = request.form['stripeEmail']
    customer = stripe.Customer.create(
        card=request.form['stripeToken'],
        email=email
    )

    amount = 199
    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Corji'
    )

    count = 1
    pile.delay(recipient_number, count, sender_name)
    return render_template('html/marketing/bomb_success.html',
                           google_analytics_id=Config.GOOGLE_ANALYTICS_ID)


@celery.task
def pile(target, count, sender):
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
        client.messages.create(
            media_url=corgi,
            to=target,
            from_=Config.TWILIO_PHONE_NUMBER
        )

    client.messages.create(
        body="This dogpile sent to you by {}.".format(sender),
        to=target,
        from_=Config.TWILIO_PHONE_NUMBER
    )


@marketing_blueprint.route("/bomb", methods=['GET'])
def bomb():
    """Much hype.  Very disruptive.  Such blurb."""
    return render_template('html/marketing/bomb.html',
                           key=Config.STRIPE_PUBLIC_KEY,
                           google_analytics_id=Config.GOOGLE_ANALYTICS_ID)
