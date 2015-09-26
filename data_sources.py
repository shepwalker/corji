# This Python file uses the following encoding: utf-8
import requests


def load_from_spreadsheet(url):
    payload = requests.get(url).json()
    raw_data = payload['feed']['entry']
    return {i['gsx$emoji']['$t']: i['gsx$url']['$t'] for i in raw_data}
