# This Python file uses the following encoding: utf-8
import imghdr
from io import BytesIO

import emoji
from PIL import Image

from corji.settings import Config

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


def get_content_type_header(response):
    """Given a requests response from an image download, attempts to
    determine the proper content-type header. Falls back to image/jpeg
    if valid header can't be found."""
    detected_content_type = imghdr.what("blerg", h=response.content)
    content_header = detected_to_header_mapping.get(
        detected_content_type, None)
    if not content_header:
        if response.headers['content-type'] in accepted_mime_types:
            return response.headers['content-type']
        else:
            return 'image/jpeg'
    else:
        return content_header


def return_image_binary(original_image_request):
    if Config.IMAGE_RESIZE:
        file_photodata = BytesIO(original_image_request.content)
        working_image = Image.open(file_photodata)
        #width, length
        original_width = working_image.size[0]
        original_length = working_image.size[1]

        if original_width > Config.IMAGE_RESIZE_PIXELS:
            resize_width = Config.IMAGE_RESIZE_PIXELS
            resize_ratio = original_width/resize_width
            resize_length = int(original_length/resize_ratio)

            working_image = working_image.resize(
                (resize_width, resize_length), resample=Image.ANTIALIAS)

        target_buffer = BytesIO()
        working_image.save(target_buffer, "JPEG")

        picture_body = target_buffer.getvalue()
        content_type = "image/jpeg"
    else:
        content_type = get_content_type_header(original_image_request)
        picture_body = original_image_request.content

    return (picture_body, content_type)


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

accepted_mime_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']

detected_to_header_mapping = {
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif'
}
