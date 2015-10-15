# This Python file uses the following encoding: utf-8
import random

import requests

# TODO: GLOBALS STILL BAD EVEN IF OBFUSCATED
corgis = {}


def load(url):
    global corgis
    payload = requests.get(url).json()
    raw_data = payload['feed']['entry']

    for row in raw_data:
        # Yes, Google's JSON is opaque and awful.
        emoji = row['gsx$emoji']['$t']
        urls = list(filter(lambda i: i != '', [
            row['gsx$url1']['$t'],
            row['gsx$url2']['$t'],
            row['gsx$url3']['$t']
        ]))
        if len(urls) > 0:
            corgis[emoji] = urls


def get_all(emoji):
    """Returns all corgis for a given emoji."""
    return corgis.get(emoji, [])

def get(emoji):
    """Returns just one corgi for a given emoji."""
    corgis = get_all(emoji)
    if corgis:
        return random.choice(corgis)
    else:
        return None


def keys():
    return list(corgis.keys())
