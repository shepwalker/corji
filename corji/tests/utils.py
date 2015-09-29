import os
import unittest

from corji.utils import text_contains_emoji

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

if __name__ == '__main__':
    unittest.main()