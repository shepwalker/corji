from corji.models.utils.phone_numbers import sanitize_phone_number
from corji.models.utils.dynamo import (
    put
)

TABLE_NAME = "corji_piles"


def new(pile_id, recipient_phone_number, sender_name,
        pile_name, timestamp):
    item = {
        'pile_id': {'S': pile_id},
        'phone_number': {'S': sanitize_phone_number(recipient_phone_number)},
        'sender_name': {'S': sender_name},
        'pile_name': {'S': pile_name},
        'timestamp': {'S': timestamp.strftime('%Y-%m-%d %H:%M:%S')},
    }
    put(TABLE_NAME, item)
    return item
