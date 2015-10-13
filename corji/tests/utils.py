# This Python file uses the following encoding: utf-8

import unittest

import requests

from corji.utils import (
    emoji_contains_skin_tone,
    text_contains_emoji, 
    get_content_type_header
)


class UtilsTestCase(unittest.TestCase):

    def test_sanity(self):
        assert True

    def test_text_contains_emoji(self):
        assert not text_contains_emoji("")
        assert not text_contains_emoji("test")
        assert not text_contains_emoji("lorem ipsum")
        assert text_contains_emoji("🏀")
        assert text_contains_emoji("🏀asd")
        assert text_contains_emoji("asd🏀")
        assert text_contains_emoji("🇫🇷")

    def test_emoji_contains_skin_tone(self):
        assert not emoji_contains_skin_tone("🏀")
        assert not emoji_contains_skin_tone("🙏")
        assert emoji_contains_skin_tone("🙏🏾")

    def test_image_identification(self):
        test_png = requests.get("http://i.imgur.com/OacBzQQ.png")
        test_jpg = request.get("https://i.imgur.com/T0vc7TU.jpg")
        test_nonsense = request.get("http://pugandchalice.com/")
        png_header = get_content_type_header(test_png)
        jpg_header = get_content_type_header(test_jpg)
        nonsense_header = get_content_type_header(test_nonsense)
        assert png_header is "image/png"
        assert jpg_header is "image/jpeg"
        assert nonsense_header is "image/jpeg"

if __name__ == '__main__':
    unittest.main()
