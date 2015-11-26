"""
Special responses to certain user text-input. Can contain images 
and/or a text response. 
"""
from collections import namedtuple

import requests

secrets = []


SecretType = namedtuple('SecretType', ['trigger', 'text', 'media'])


def load(url):
    global piles
    payload = requests.get(url).json()
    raw_data = payload['feed']['entry']

    for row in raw_data:
        trigger = row['gsx$trigger']['$t'].strip().lower()
        text = row['gsx$text']['$t']
        media = row['gsx$media']['$t']
        secrets.append(SecretType(trigger, text, media))


def get_secret(possible_trigger):
    """Returns relevant secret or none"""
    relevant_secrets = [s for s in secrets if s.trigger == possible_trigger.strip().lower()]
    matched_secret = relevant_secrets[0] if relevant_secrets else None
    return matched_secret
