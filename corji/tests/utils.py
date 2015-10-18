# This Python file uses the following encoding: utf-8
from io import BytesIO
import os
import unittest

from PIL import Image

import requests

from corji.utils import (
    emoji_contains_skin_tone,
    emoji_is_numeric,
    get_content_type_header,
    text_contains_emoji,
    resize_image
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
        assert text_contains_emoji("3️⃣")

    def test_emoji_contains_skin_tone(self):
        assert not emoji_contains_skin_tone("🏀")
        assert not emoji_contains_skin_tone("🙏")
        assert emoji_contains_skin_tone("🙏🏾")

    def test_image_identification(self):
        test_png = requests.get("http://i.imgur.com/OacBzQQ.png")
        test_jpg = requests.get("https://i.imgur.com/T0vc7TU.jpg")
        test_nonsense = requests.get("http://pugandchalice.com/")
        png_header = get_content_type_header(test_png)
        jpg_header = get_content_type_header(test_jpg)
        nonsense_header = get_content_type_header(test_nonsense)
        assert jpg_header == "image/jpeg"
        assert png_header == "image/png"
        assert nonsense_header == "image/jpeg"

    def test_image_resize(self):
        os.environ["IMAGE_RESIZE_PIXELS"] = str(150)
        test_jpg = requests.get("https://i.imgur.com/qRWH5.jpg")
        image = resize_image(test_jpg.content)
        file_photodata = BytesIO(image)
        working_image = Image.open(file_photodata)
        edited_width = working_image.size[0]
        print(edited_width)
        assert edited_width == 300

    def test_emoji_is_numeric(self):
        assert not emoji_is_numeric("🏀")
        assert emoji_is_numeric("3️⃣")

if __name__ == '__main__':
    unittest.main()
