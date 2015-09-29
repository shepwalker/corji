# This Python file uses the following encoding: utf-8

import emoji


def text_contains_emoji(text):
    for char in text:
        if emoji.demojize(char) != char:
            return True

    # Edge case: check for flags as they're represented
    # as multiple characters: https://en.wikipedia.org/wiki/Regional_Indicator_Symbol
    if len(text) == 2:
        spaced_string = "{} {}".format(text[0], text[1])
        if emoji.demojize(spaced_string) != spaced_string:
            return True

    return False
