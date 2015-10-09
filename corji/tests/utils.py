# This Python file uses the following encoding: utf-8

import unittest

from corji.utils import (
    emoji_contains_skin_tone,
    text_contains_emoji
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

if __name__ == '__main__':
    unittest.main()
