"""Views that hit Stripe."""
from flask import Blueprint, render_template, request
import stripe

from corji import settings
from corji.models import emoji_customer

stripe.api_key = settings.Config.STRIPE_SECRET_KEY
stripe_blueprint = Blueprint('stripe', __name__,
                             template_folder='templates')


@stripe_blueprint.route('/stripe')
def request_charge():
    return render_template('html/stripe/stripe.html',
                           key=settings.Config.STRIPE_PUBLIC_KEY,
                           phone_number=request.values.get('phone_number'),
                           recharge_count=settings.Config.CONSUMPTIONS_PER_RECHARGE,
                           recharge_price=settings.Config.RECHARGE_PRICE)


@stripe_blueprint.route('/charge', methods=['GET'])
def process_charge():

    email = request.form['stripeEmail']
    customer = stripe.Customer.create(
        card=request.form['stripeToken'],
        email=email
    )

    amount = settings.Config.RECHARGE_PRICE
    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Corji'
    )

    phone_number = request.form['phone_number']

    emoji_customer.modify_consumptions(phone_number, settings.Config.CONSUMPTIONS_PER_RECHARGE)
    emoji_customer.add_metadata(phone_number, 'email', email)

    return render_template('html/stripe/stripe_success.html')
