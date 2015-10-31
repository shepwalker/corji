import random

from twilio.rest import TwilioRestClient

from corji.api import CorgiResource
from corji.data_sources import (
    google_spreadsheets
)
from corji.settings import Config

api = CorgiResource()
client = TwilioRestClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

number_of_corgis_to_send = 3
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
        to="+18046989478",
        from_=Config.TWILIO_PHONE_NUMBER
    )
