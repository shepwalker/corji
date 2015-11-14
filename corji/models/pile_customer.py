import boto3

from corji.models.utils.phone_numbers import sanitize_phone_number
from corji.settings import Config


dynamo_client = boto3.client("dynamodb", region_name=Config.AWS_DEFAULT_REGION)

TABLE_NAME = "corji_piles"


def put(item):
    dynamo_client.put_item(
        TableName=TABLE_NAME,
        Item=item
    )


def new(pile_id, recipient_phone_number, sender_name,
        pile_name, timestamp):
    item = {
        'pile_id': {'S': pile_id},
        'phone_number': {'S': sanitize_phone_number(recipient_phone_number)},
        'sender_name': {'S': sender_name},
        'pile_name': {'S': pile_name},
        'timestamp': {'S': timestamp.strftime('%Y-%m-%d %H:%M:%S')},
    }
    put(item)
    return item
