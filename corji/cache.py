# This Python file uses the following encoding: utf-8
import os
import urllib.request

import emoji

from corji.app import app
from corji.exceptions import CorgiNotFoundException
from corji.settings import Config

logger = app.logger


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
