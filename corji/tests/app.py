# This Python file uses the following encoding: utf-8

import unittest

from corji.app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_sanity(self):
        assert True

    def test_fallback_message(self):
        response = self.app.get('/')
        assert 'Welcome to Corji' in str(response.data)

    def test_happy_case_emoji(self):
        response = self.app.post('/', data={
            'From': '+15556667777',
            'Body': '😀'}
        )
        assert 'http' in str(response.data)

    def test_sad_case_emoji(self):
        response = self.app.post('/', data={
            'From': '+15556667777',
            'Body': '🔶'}
        )
        assert 'http' in str(response.data)
        assert '.jpg' in str(response.data)
        assert ':(' in str(response.data)

    def test_emoticon_support(self):
        response = self.app.post('/', data={
            'From': '+15556667777',
            'Body': ':D'}
        )
        assert 'http' in str(response.data)
        assert '.jpg' in str(response.data)
        assert ':(' not in str(response.data)


if __name__ == '__main__':
    unittest.main()
