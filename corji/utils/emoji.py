import emoji


def text_contains_emoji(text):
    for char in text:
        if emoji.demojize(char) != char:
            return True

    # Edge case: check for flags as they're represented as multiple chars:
    # https://en.wikipedia.org/wiki/Regional_Indicator_Symbol
    if len(text) == 2:
        spaced_string = "{} {}".format(text[0], text[1])
        if emoji.demojize(spaced_string) != spaced_string:
            return True

    # Check for the numeric emoji things.
    if emoji_is_numeric(text):
        return True

    return False


def emoji_contains_skin_tone(text):
    # Naive check for a two-char string,
    # with the second char being the skin tone modifier.
    # Deetz here: http://www.unicode.org/reports/tr51/tr51-2.html#Diversity
    skin_tone_characters = [
        '\U0001f3fb',
        '\U0001f3fc',
        '\U0001f3fd',
        '\U0001f3fe',
        '\U0001f3ff'
    ]

    if len(text) == 1:
        return False

    return text[1] in skin_tone_characters


def emoji_is_numeric(text):
    return len(text) > 1 and text[0] in '1234567890'

emojis_for_emoticons = {
    ':D': '😀',
    ':)': '😊',
    ':(': '😞',
    ':P': '😜',
    '=)': '😃',
    '=(': '😞',
    '=P': '😜',
    ';)': '😉',
    'XD': '😝',
    '<3': '❤️',
    ':|': '😐',
    ':o': '😮',
    ':3': '😙',
    '(Y)': '👍',
    '^_^': '😸',
    '>_<': '😣',
    'B-)': '😎'
}
