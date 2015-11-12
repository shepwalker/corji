# This Python file uses the following encoding: utf-8
import unittest

from corji.app import app


class MarketingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_about(self):
        response = self.app.get('/')
        assert "Corji" in str(response.data)

    def test_pile(self):
        response = self.app.get('/pile')

        # Haven't actually implemented this.
        pass


if __name__ == '__main__':
    unittest.main()
