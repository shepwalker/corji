# This Python file uses the following encoding: utf-8

import emoji


def text_contains_emoji(text):
	for char in text:
		if emoji.demojize(char) != char:
			return True
	return False


def singleton(cls, *args):
    instances = {}
    def get_instance(*args):
        if cls not in instances:
            instances[cls] = cls(args)
        return instances[cls]
    return get_instance(*args)