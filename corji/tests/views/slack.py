import unittest

from corji.app import app


class SlackTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_slack_happy_case(self):
        response = self.app.get('/slack?text=🏀')
        assert 'image_url' in str(response.data)
        assert 'in_channel' in str(response.data)

    def test_slack_sad_case(self):
        response = self.app.get('/slack?text=💩')
        assert 'in_channel' not in str(response.data)
        assert 'Oh' in str(response.data)
