# This Python file uses the following encoding: utf-8
import unittest

from corji.api import CorgiResource


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = CorgiResource()

    def test_sanity(self):
        assert True

    def test_get_random(self):
        response = self.api.get()
        assert response is not None
        assert response["count"] is not None
        assert response["emoji"] is not None
        assert response["results"] is not None
        assert response["count"] == len(response["results"])
        assert response["count"] > 0

    def test_get_basic(self):
        response = self.api.get('🌈')
        assert response is not None
        assert response["count"] is not None
        assert response["emoji"] == '🌈'
        assert response["results"] is not None
        assert response["count"] == len(response["results"])
        assert response["count"] > 0

    def test_get_multiple_results(self):
        response = self.api.get('🐗')
        assert response is not None
        assert response["count"] > 1
        assert response["emoji"] == '🐗'
        assert len(response["results"]) > 1

    def test_get_non_emoji_input(self):
        response = self.api.get('ham sandwich')
        assert response is not None
        assert response["count"] == 0
        assert response["emoji"] == ''
        assert response["results"] == []

    def test_get_should_not_return_broken_links(self):
        response = self.api.get('🌿')
        assert response["count"] == 0
        assert response["emoji"] == '🌿'
        assert response["results"] == []
