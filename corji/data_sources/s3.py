# This Python file uses the following encoding: utf-8
import logging
import random
from urllib.error import HTTPError

from io import BytesIO

import boto3
import boto3.s3
from botocore.vendored.requests.exceptions import ConnectionError
import emoji
from PIL import Image
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError

from corji.exceptions import CorgiNotFoundException
from corji.settings import Config
from corji.utils import (
    get_content_type_header,
    return_image_binary
)

logger = logging.getLogger(Config.LOGGER_NAME)


aws_s3_client = None
all_objects = []
pre_auth_URLS = {}


def load():
    global aws_s3_client, all_objects
    aws_s3_client = boto3.client("s3")
    all_objects = aws_s3_client.list_objects(
        Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)
    for obj in all_objects['Contents']:
        possible_url = aws_s3_client.generate_presigned_url(
            'get_object', ExpiresIn=31540000, Params={
                'Bucket': Config.AWS_S3_CACHE_BUCKET_NAME,
                'Key': obj['Key'],
            }
        )
        pre_auth_URLS[obj['Key']] = possible_url

# TODO: delete_all()
# TODO: Also create put().


def put_all(corgis):
    cacheable_corgis = [corgi for corgi in corgis if corgis[corgi]]
    for emoji in cacheable_corgis:
        corgi_list = corgis[emoji]

        for i, corgi in enumerate(corgi_list):
            s3_key = get_file_name_from_emoji(i, emoji)

            # see if this corgi already exists in s3 bucket
            if 'Contents' in all_objects:
                possible_s3_entry = next(
                    (item for item in all_objects['Contents'] if item['Key'] == s3_key), None)
            else:
                possible_s3_entry = None
            try:
                if not possible_s3_entry:
                    logger.debug("Adding %s to remote cache", s3_key)
                    logger.debug(
                        "Downloading corgi %s in prep for remote cache", corgi)
                    picture_request = requests.get(corgi)
                    image_data = return_image_binary(picture_request)

                    picture_body = image_data[0]
                    content_type = image_data[1]

                    logger.debug("Adding %s to remote cache", s3_key)

                    aws_s3_client.put_object(Body=picture_body,
                                             ContentType=content_type,
                                             Key=s3_key,
                                             Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)

                else:
                    logger.debug("%s found in remote cache. Skipping", s3_key)

            except (HTTPError, ConnectionError, requests.exceptions.ConnectionError) as e:
                logger.error(
                    "Http error occurred while creating remote cache on %s", s3_key, e)
            except (OSError) as e:
                logger.error("OSError Occurred during resizing", e)


def get_all(raw_emoji):
    folder_name = emoji.demojize(raw_emoji).replace(":", "")
    possible_s3_entries = [
        item for item in all_objects['Contents'] if folder_name in item['Key']]

    if possible_s3_entries:
        urls = []
        for entry in possible_s3_entries:
            url = pre_auth_URLS[entry['Key']]
            urls.append(url)
        return urls
    else:
        raise CorgiNotFoundException("Corgi not found in remote store for emoji: {}"
                                     .format(raw_emoji))


def get(emoji):
    """Returns just one corgi for a given emoji."""
    corgis = get_all(emoji)
    if corgis:
        return random.choice(corgis)
    else:
        return None


def get_file_name_from_emoji(i, raw_emoji):
    return emoji.demojize(raw_emoji).replace(":", "") + "/0{}.jpg".format(i + 1)
