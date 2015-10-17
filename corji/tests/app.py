# This Python file uses the following encoding: utf-8

import unittest

from corji.app import app


# TODO: actually relying on the SPREADSHEET_URL is a codesmell.
class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def send_message_with_body(self, body):
        return self.app.post('/sms', data={
            'From': '+15556667777',
            'Body': body}
        )

    def test_sanity(self):
        assert True

    def test_fallback_message(self):
        response = self.app.get('/sms')
        assert 'Welcome to Corji' in str(response.data)

    def test_failure_fallback(self):
        response = self.app.get('/sms/fallback')
        assert 'Sorry' in str(response.data)
        assert 'http' in str(response.data)

    def test_happy_case_emoji(self):
        response = self.send_message_with_body('🌈')
        assert 'http' in str(response.data)
        assert ':(' not in str(response.data)

    def test_skin_tone_emoji(self):
        response = self.send_message_with_body('🙏🏾')
        base_response = self.send_message_with_body('🙏')

        assert response.data == base_response.data

    def test_sad_case_emoji(self):
        response = self.send_message_with_body('🔶')
        assert 'http' in str(response.data)
        assert string_contains_image(response.data)
        assert ':(' in str(response.data)

    def test_emoticon_support(self):
        response = self.send_message_with_body(':D')
        assert 'http' in str(response.data)
        assert string_contains_image(response.data)
        assert ':(' not in str(response.data)

    def test_trailing_whitespace_should_be_stripped(self):
        response = self.send_message_with_body('🌈  ')
        assert 'http' in str(response.data)
        assert ':(' not in str(response.data)

    def test_leading_whitespace_should_be_stripped(self):
        response = self.send_message_with_body('    🌈')
        assert 'http' in str(response.data)
        assert ':(' not in str(response.data)


def string_contains_image(image_string):
    return (
        '.jpg' in str(image_string) or
        '.gif' in str(image_string) or
        '.png' in str(image_string) or
        'gstatic.com' in str(image_string)
    )

if __name__ == '__main__':
    unittest.main()
