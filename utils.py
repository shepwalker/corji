# This Python file uses the following encoding: utf-8

import emoji


def text_contains_emoji(text):
	for char in text:
		if emoji.demojize(char) != char:
			return True
	return False