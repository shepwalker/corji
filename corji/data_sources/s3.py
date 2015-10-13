# This Python file uses the following encoding: utf-8
import logging
from urllib.error import HTTPError


import boto3
import boto3.s3
from botocore.vendored.requests.exceptions import ConnectionError
import emoji
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError

from corji.exceptions import CorgiNotFoundException
from corji.settings import Config
from corji.utils import (
    get_content_type_header
)

logger = logging.getLogger(Config.LOGGER_NAME)

aws_s3_client = boto3.client("s3")
all_objects = aws_s3_client.list_objects(Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)


def put_all(corgis):
   
    cacheable_corgis = [corgi for corgi in corgis if corgis[corgi]]
    for i in cacheable_corgis:
        corgi = corgis[i]

        s3_key = get_file_name_from_emoji(i)

        # see if this corgi already exists in s3 bucket
        if 'Contents' in all_objects:
            possible_s3_entry = next(
                (item for item in all_objects['Contents'] if item['Key'] == s3_key), None)
        else:
            possible_s3_entry = None
        try:
            if not possible_s3_entry:
                logger.debug("Adding %s to remote cache", i)
                logger.debug("Downloading corgi %s in prep for remote cache", i)
                picture_request = requests.get(corgi)
                logger.debug("Adding %s to remote cache", i)
                content_type = get_content_type_header(picture_request)
                
                aws_s3_client.put_object(Body=picture_request.content,
                                         ContentType=content_type,
                                         Key=s3_key,
                                         Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)

            else:
                logger.debug("%s found in remote cache. Skipping", i)

        except (HTTPError, ConnectionError, requests.exceptions.ConnectionError) as e:
            logger.error(
                "Http error occurred while creating remote cache on %s", i, e)


def get(raw_emoji):
    possible_s3_key = get_file_name_from_emoji(raw_emoji)
    possible_s3_entry = next(
        (item for item in all_objects['Contents'] if item['Key'] == possible_s3_key), None)

    if possible_s3_entry:
        possible_url = aws_s3_client.generate_presigned_url(
            'get_object', Params={'Bucket': Config.AWS_S3_CACHE_BUCKET_NAME,
                                  'Key': possible_s3_key}
        )
        return possible_url
    else:
        raise CorgiNotFoundException("Corgi not found in remote store for emoji: {}"
                                     .format(raw_emoji))


def get_file_name_from_emoji(raw_emoji):
    return emoji.demojize(raw_emoji).replace(":", "") + "/01.jpg"
