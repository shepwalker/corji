import boto3

dynamo_client = boto3.client("dynamodb", region_name="us-west-1")

TABLE_NAME = "corji"


def get(phone_number):
    response = dynamo_client.get_item(
        TableName=TABLE_NAME,
        Key={'phone_number': {'S': phone_number}}
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


def increment_consumptions(phone_number):
    dynamo_client.update_item(
        TableName=TABLE_NAME,
        Key={'phone_number': {"S": phone_number}},
        AttributeUpdates={"consumptions": {"Action": "ADD", "Value": {"N": "1"}}})


def new(phone_number):
    item = {
        'phone_number': {'S': phone_number},
        'consumptions': {'N': '1'}
    }
    put(item)
