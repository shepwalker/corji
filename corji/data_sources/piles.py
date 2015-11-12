from collections import namedtuple

import requests

piles = []


PileType = namedtuple('PileType', ['name', 'emojis'])


def load(url):
    global piles
    payload = requests.get(url).json()
    raw_data = payload['feed']['entry']

    for row in raw_data:
        name = row['gsx$name']['$t']
        emojis = row['gsx$emojis']['$t']
        piles.append(PileType(name, emojis))
