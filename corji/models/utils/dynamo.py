import boto3

from corji.settings import Config

dynamo_client = boto3.client("dynamodb", region_name=Config.AWS_DEFAULT_REGION)


def put(table_name, item):
    dynamo_client.put_item(
        TableName=table_name,
        Item=item
    )
