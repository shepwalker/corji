# This Python file uses the following encoding: utf-8
from io import BytesIO
import logging
import random
from urllib.error import HTTPError

import boto3
import boto3.s3
from botocore.vendored.requests.exceptions import ConnectionError
import emoji
from PIL import Image
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError

from corji.exceptions import CorgiNotFoundException
from corji.settings import Config
from corji.utils.image_utils import (
    get_content_type_header,
    resize_image
)

logger = logging.getLogger(Config.LOGGER_NAME)


aws_s3_client = None
all_objects = []
pre_auth_URLS = {}


def load():
    global aws_s3_client, all_objects
    aws_s3_client = boto3.client("s3")

    # TODO: silently fail if we don't have the thing.
    all_objects = aws_s3_client.list_objects(Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)


    if 'Contents' in all_objects:
        for obj in all_objects['Contents']:
            possible_url = aws_s3_client.generate_presigned_url(
                'get_object', ExpiresIn=31540000, Params={
                    'Bucket': Config.AWS_S3_CACHE_BUCKET_NAME,
                    'Key': obj['Key'],
                }
            )
            pre_auth_URLS[obj['Key']] = possible_url

# TODO: delete_all()
def put_all(corgis):
    cacheable_corgis = [corgi for corgi in corgis if corgis[corgi]]
    for emoji in cacheable_corgis:
        put(emoji, corgis)


def put(emoji, corgis):
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
                logger.debug("Downloading corgi %s in prep for remote cache", corgi)
                picture_request = requests.get(corgi)
                logger.debug("Adding %s to remote cache", s3_key)
                content_type = get_content_type_header(picture_request)

                aws_s3_client.put_object(Body=picture_request.content,
                                         ContentType=content_type,
                                         Key=s3_key,
                                         Bucket=Config.AWS_S3_CACHE_BUCKET_NAME)

            else:
                possible_s3_entry = None
            try:
                if not possible_s3_entry:
                    logger.debug("Adding %s to remote cache", s3_key)
                    logger.debug(
                        "Downloading corgi %s in prep for remote cache", corgi)
                    picture_request = requests.get(corgi)
                    picture_body = None
                    content_type = None
                    if Config.IMAGE_RESIZE:
                            file_photodata = BytesIO(picture_request.content)
                            working_image = Image.open(file_photodata)
                            #width, length
                            original_width = working_image.size[0]
                            

                            if original_width > Config.IMAGE_RESIZE_PIXELS:
                                picture_body = resize_image(picture_request.content)
                                content_type = "image/jpeg"
                    
                    if not picture_body:
                        content_type = get_content_type_header(picture_request)
                        picture_body = picture_request.content
                    
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
        except OSError as e:
            logger.error("OSError Occurred during resizing", e)


def get_all(raw_emoji):
    folder_name = emoji.demojize(raw_emoji).replace(":", "")
    possible_s3_entries = [
        item for item in all_objects['Contents'] if folder_name in item['Key']]

    if possible_s3_entries:
        urls = []
        for entry in possible_s3_entries:
            url = pre_auth_URLS.get(entry['Key'], None)
            if not url:
                url = aws_s3_client.generate_presigned_url(
                'get_object', Params={'Bucket': Config.AWS_S3_CACHE_BUCKET_NAME,
                                     'Key': entry['Key']}
                )
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
