# This Python file uses the following encoding: utf-8
import os
import urllib.request

import emoji

from exceptions import CorgiNotFoundException

CACHE_DIR = os.getenv('CORJI_CACHE_PATH', './cache')


def put_in_local_cache(corgis):
    for i in corgis:
        corgi = corgis.get(i, None)
        if not corgi:
            continue

        emoji_dir = emoji.demojize(i).replace(":", "")
        try:
            directory = CACHE_DIR + '/' + emoji_dir
            if not os.path.exists(directory):
                os.makedirs(directory)
                urllib.request.urlretrieve(corgi, directory + "/01.jpg")
        except:
            print("Failed on: " + i)


def get_from_local_cache(raw_emoji):
    filename = emoji.demojize(raw_emoji).replace(":", "")
    cached_filename = CACHE_DIR + "/" + filename
    split_name = filename.split('/')
    if(os.path.exists(cached_filename)):
        return CACHE_DIR + "/" + split_name[0] + "/01.jpg"
    else:
        raise CorgiNotFoundException("Corgi not found for emoji: {}".format(raw_emoji))
