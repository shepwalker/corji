"""Views that hit Stripe."""
from flask import Blueprint, render_template, request
import stripe

from corji import (
    customer_data,
    settings
)

stripe.api_key = settings.Config.STRIPE_SECRET_KEY
stripe_blueprint = Blueprint('stripe', __name__,
                             template_folder='templates')


@stripe_blueprint.route('/stripe')
def request_charge():
    return render_template('html/stripe.html',
                           key=settings.Config.STRIPE_PUBLIC_KEY,
                           phone_number=request.values.get('phone_number'),
                           recharge_count=settings.Config.CONSUMPTIONS_PER_RECHARGE,
                           recharge_price=settings.Config.RECHARGE_PRICE)


@stripe_blueprint.route('/charge', methods=['POST'])
def process_charge():

    customer = stripe.Customer.create(
        card=request.form['stripeToken']
    )

    amount = settings.Config.RECHARGE_PRICE
    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Corji'
    )

    phone_number = request.form['phone_number']
    customer_data.modify_consumptions(phone_number, settings.Config.CONSUMPTIONS_PER_RECHARGE)

    return render_template('html/stripe_success.html')
