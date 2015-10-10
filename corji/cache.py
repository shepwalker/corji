# This Python file uses the following encoding: utf-8
import logging
from urllib.error import HTTPError


import boto3
import boto3.s3
import emoji
import requests

from corji.exceptions import CorgiNotFoundException
from corji.settings import Config

logger = logging.getLogger(Config.LOGGER_NAME)

if (Config.REMOTE_CACHE_POPULATE or 
    Config.REMOTE_CACHE_RETRIEVE):
    aws_s3_client = boto3.client("s3")
    all_objects = aws_s3_client.list_objects(
        Bucket = Config.AWS_S3_CACHE_BUCKET_NAME)


def put_in_remote_cache(corgis):
    for i in corgis:
        corgi = corgis[i]
        if not corgi:
            continue

        # redundant but need the directory path to confirm it
        # exists and such
        emoji_dir = emoji.demojize(i).replace(":", "")
        directory = Config.CACHE_DIR + '/' + emoji_dir

        s3_key = get_file_name_from_emoji(i)

        # see if this corgi already exists in s3 bucket
        #print(all_objects)
        if 'Contents' in all_objects:
            possible_s3_entry = next(
                (item for item in all_objects['Contents'] if item['Key'] == s3_key), None)
        else:
            possible_s3_entry = None
        try:
            if not possible_s3_entry:
                logger.debug("Adding %s to remote cache", i)
                logger.debug(
                        "Downloading corgi %s in prep for remote cache", i)
                picture_request = requests.get(corgi)
                logger.debug("Adding %s to remote cache", i)
                aws_s3_client.put_object(Body = picture_request.content, ContentType = "image/jpeg", 
                  Key = s3_key, Bucket = Config.AWS_S3_CACHE_BUCKET_NAME)

            else:
                logger.debug("%s found in remote cache. Skipping", i)
        except HTTPError:
            logger.error(
                "Http error occurred while creating remote cache on %s", i)


def get_from_remote_cache(raw_emoji):

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
    return  emoji.demojize(raw_emoji).replace(":", "") + "/01.jpg"
