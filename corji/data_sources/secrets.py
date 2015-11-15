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
