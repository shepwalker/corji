"""
Supplement data for message or user-specific data.
"""
from collections import namedtuple

import requests

supplements = []


SupplementType = namedtuple('SupplementType', ['Name','TriggerType', 'Param', 'Text', 'Media'])


def load(url):
    global piles
    payload = requests.get(url).json()
    raw_data = payload['feed']['entry']

    for row in raw_data:
        trigger_type = row['gsx$triggertype']['$t'].strip().lower()
        param = row['gsx$param']['$t']
        text = row['gsx$text']['$t']
        media = row['gsx$media']['$t'] or ""
        name = row['gsx$name']['$t']

        supplements.append(SupplementType(name, trigger_type, param, text, media)) 


def get_supplement(possible_trigger):
	"""Returns relevant supplement or none"""
	relevant_supplement = [s for s in supplements if s.trigger == possible_trigger.strip().lower()]
	matched_supplement = relevant_indexes[0] if relevant_indexes else None
	return matched_supplement

def get_all():
    return supplements