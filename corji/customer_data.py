import boto3

from corji.settings import Config

dynamo_client = boto3.client("dynamodb", region_name=Config.AWS_DEFAULT_REGION)

TABLE_NAME = Config.AWS_DYNAMO_TABLE_NAME


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
        Item=item, 
    )


def add_metadata(phone_number, key, value):
    dynamo_client.update_item(
        TableName=TABLE_NAME,
        Key={
            'phone_number': {"S": sanitize_phone_number(phone_number)}
        },
        AttributeUpdates={
            key: {
                "Action": "PUT",
                "Value": {"S": str(value)}
            }
        }
    )


def modify_consumptions(phone_number, consumptions=1):
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
        'consumptions': {'N': str(Config.FREE_CONSUMPTIONS)}
    }
    put(item)
    return item
