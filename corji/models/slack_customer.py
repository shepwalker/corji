from corji.models.utils.dynamo import (
    dynamo_client,
    put
)


# Normally this should be something more specific -- but legacy reasons.
TABLE_NAME = "corji_slack"


def get(team_id):
    response = dynamo_client.get_item(
        TableName=TABLE_NAME,
        Key={'team_id': {'S': team_id}}
    )
    return response.get('Item', None)


def add_metadata(team_id, key, value):
    dynamo_client.update_item(
        TableName=TABLE_NAME,
        Key={
            'team_id': {"S": team_id}
        },
        AttributeUpdates={
            key: {
                "Action": "PUT",
                "Value": {"S": str(value)}
            }
        }
    )


def new(team_id, access_token, team_name):
    item = {
        'team_id': {'S': team_id},
        'access_token': {'S': access_token},
        'team_name': {'S': team_name}
    }
    put(TABLE_NAME, item)
    return item
