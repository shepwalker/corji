from io import BytesIO
import os

import unittest
from PIL import Image
import requests

from corji.utils.emoji import (
    emoji_contains_skin_tone,
    emoji_is_numeric,
    text_contains_emoji,
)


class EmojiUtilsTestCase(unittest.TestCase):
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

    def test_emoji_is_numeric(self):
        assert not emoji_is_numeric("🏀")
        assert emoji_is_numeric("3️⃣")


if __name__ == '__main__':
    unittest.main()