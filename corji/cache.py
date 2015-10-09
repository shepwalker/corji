# This Python file uses the following encoding: utf-8
import os
import logging
from urllib import request
from urllib.error import HTTPError


import emoji
import boto3
import boto3.s3
from boto3.s3.transfer import S3Transfer


from corji.exceptions import CorgiNotFoundException
from corji.settings import Config

logger = logging.getLogger(Config.LOGGER_NAME)

if (Config.REMOTE_CACHE_POPULATE_ENABLED or 
    Config.REMOTE_CACHE_RETRIEVE_ENABLED):
    aws_s3_client = boto3.client("s3")
    all_objects = aws_s3_client.list_objects(
        Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)


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
        if 'Content' in all_objects:
            possible_s3_entry = next(
                (item for item in all_objects['Contents'] if item['Key'] == s3_key), None)
        else:
            possible_s3_entry = None
        try:

            if not possible_s3_entry:
                # edge case if corgi doesn't exist in s3 but
                # somehow directory exists locally
                if not os.path.exists(directory):
                    os.makedirs(directory)
                local_file_target = directory + "/01.jpg"
                # edge case if corgi doesn't exist in s3 but
                # somehow  exists locally
                if not os.path.exists(local_file_target):
                    logger.debug(
                        "Downloading corgi %s in prep for remote cache", i)
                    request.urlretrieve(corgi, directory + "/01.jpg")
                logger.debug("Adding %s to remote cache", i)
                transfer_s3_client = S3Transfer(aws_s3_client)
                transfer_s3_client.upload_file(
                    directory+"/01.jpg", Config.AWS_S3_CACHE_BUCKET_NAME, s3_key, extra_args={'ContentType': "image/jpeg"})
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
            'get_object', Params={'Bucket': Config.AWS_S3_CACHE_BUCKET_NAME, 'Key': possible_s3_key})
        return possible_url
    else:
        raise CorgiNotFoundException("Corgi not found in remote store for emoji: {}"
                                     .format(raw_emoji))

def get_file_name_from_emoji(raw_emoji):
    return  emoji.demojize(raw_emoji).replace(":", "") + "/01.jpg"