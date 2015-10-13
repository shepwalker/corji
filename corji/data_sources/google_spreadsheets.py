# This Python file uses the following encoding: utf-8
import requests

# TODO: GLOBALS STILL BAD EVEN IF OBFUSCATED
corgis = {}


def load(url):
    global corgis
    payload = requests.get(url).json()
    raw_data = payload['feed']['entry']
    corgis = {i['gsx$emoji']['$t']: i['gsx$url']['$t'] for i in raw_data}


def get(emoji):
    return corgis.get(emoji, None)


def keys():
    return [i for i in corgis if corgis[i] != '']
