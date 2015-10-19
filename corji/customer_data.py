import boto3

from corji.settings import Config

dynamo_client = boto3.client("dynamodb", region_name="us-west-1")

TABLE_NAME = Config.AWS_S3_CACHE_BUCKET_NAME


def sanitize_phone_number(phone_number):
    return phone_number.strip("+").strip()


def get(phone_number):
    response = dynamo_client.get_item(
        TableName=TABLE_NAME,
        Key={'phone_number': {'S': sanitize_phone_number(phone_number)}}
    )
    if 'Item' in response:
        return response['Item']
    else:
        return None


def put(item):
    dynamo_client.put_item(
        TableName=TABLE_NAME,
        Item=item
    )


def increment_consumptions(phone_number, consumptions):
    dynamo_client.update_item(
        TableName=TABLE_NAME,
        Key={
            'phone_number': {"S": sanitize_phone_number(phone_number)}
        },
        AttributeUpdates={
            "consumptions": {
                "Action": "ADD",
                "Value": {"N": str(consumptions)}
            }
        }
    )


def decrement_consumptions(phone_number, consumptions=1):
    dynamo_client.update_item(
        TableName=TABLE_NAME,
        Key={
            'phone_number': {"S": sanitize_phone_number(phone_number)}
        },
        AttributeUpdates={
            "consumptions": {
                "Action": "ADD",
                "Value": {"N": str(consumptions * -1)}
            }
        }
    )


def new(phone_number):
    item = {
        'phone_number': {'S': sanitize_phone_number(phone_number)},
        'consumptions': {'N': '19'}
    }
    put(item)
