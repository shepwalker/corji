# This Python file uses the following encoding: utf-8
import os
from urllib import request
from urllib.error import HTTPError

import emoji
import boto3
import boto3.s3
from boto3.s3.transfer import S3Transfer

from corji.app import app
from corji.exceptions import CorgiNotFoundException
from corji.settings import Config

logger = app.logger

if Config.REMOTE_CACHE_POPULATE_ENABLED or
    Config.REMOTE_CACHE_RETRIEVE_ENABLED:
    aws_s3_client = boto3.client("s3")
    all_objects = aws_s3_client.list_objects(
        Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)


def put_in_local_cache(corgis):
    for i in corgis:
        corgi = corgis.get(i, None)
        if not corgi:
            continue

        emoji_dir = emoji.demojize(i).replace(":", "")
        try:
            directory = Config.CACHE_DIR + '/' + emoji_dir
            if not os.path.exists(directory):
                os.makedirs(directory)
                urllib.request.urlretrieve(corgi, directory + "/01.jpg")
        except:
            logger.error("Failed on: " + i)


def get_from_local_cache(raw_emoji):
    filename = emoji.demojize(raw_emoji).replace(":", "")
    cached_filename = Config.CACHE_DIR + "/" + filename
    split_name = filename.split('/')
    if(os.path.exists(cached_filename)):
        return Config.CACHE_DIR + "/" + split_name[0] + "/01.jpg"
    else:
        raise CorgiNotFoundException("Corgi not found for emoji: {}"
                                     .format(raw_emoji))


def put_in_remote_cache(corgis):
    for i in corgis:
        corgi = corgis.get(i, None)
        if not corgi:
            continue

        emoji_dir = emoji.demojize(i).replace(":", "")

        directory = Config.CACHE_DIR + '/' + emoji_dir
        s3_key = emoji_dir + "/01.jpg"
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
    filename = emoji.demojize(raw_emoji).replace(":", "")

    possible_s3_key = filename + "/01.jpg"
    possible_s3_entry = next(
        (item for item in all_objects['Contents'] if item['Key'] == possible_s3_key), None)

    if possible_s3_entry:
        possible_url = aws_s3_client.generate_presigned_url(
            'get_object', Params={'Bucket': Config.AWS_S3_CACHE_BUCKET_NAME, 'Key': possible_s3_key})
        return possible_url
    else:
        raise CorgiNotFoundException("Corgi not found for emoji: {}"
                                     .format(raw_emoji))
