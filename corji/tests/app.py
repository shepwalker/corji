# This Python file uses the following encoding: utf-8
import random
import unittest

from corji.app import app
from corji.models import emoji_customer
from corji.settings import Config


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def send_message_with_body(self, body, phone_number=random.random()):
        return self.app.post('/sms', data={
            'From': '{}'.format(phone_number),
            'Body': body}
        )

    def test_sanity(self):
        assert True

    def test_fallback_message(self):
        response = self.send_message_with_body("")
        assert 'Welcome to Corji' in str(response.data)

    def test_failure_fallback(self):
        response = self.app.get('/sms/fallback')
        assert 'Sorry' in str(response.data)
        assert 'http' in str(response.data)

    def test_voice_fallback(self):
        response = self.app.get('/voice')
        assert 'Try texting this number' in str(response.data)
        assert 'Say' in str(response.data)

    def test_happy_case_emoji(self):
        response = self.send_message_with_body('🌈')
        assert 'http' in str(response.data)
        assert ':(' not in str(response.data)

    def test_skin_tone_emoji(self):
        response = self.send_message_with_body('🙏🏾')
        base_response = self.send_message_with_body('🙏')

        assert ".jpg" in str(response.data)
        assert ".jpg" in str(base_response.data)
        assert ":(" not in str(response.data)
        assert ":(" not in str(base_response.data)

    def test_sad_case_emoji(self):
        response = self.send_message_with_body('🔸')
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

    def test_numeric_emojis_should_be_happy(self):
        response = self.send_message_with_body('6️⃣')
        assert 'http' in str(response.data)
        assert ':(' not in str(response.data)

    def test_should_not_return_broken_links(self):
        response = self.send_message_with_body('🌿')
        assert 'http' in str(response.data)
        assert ':(' in str(response.data)
        assert 'not-a-url' not in str(response.data)

    def test_stop_case(self):
        phone_number = random.random()
        response = self.send_message_with_body('stop', phone_number=phone_number)
        assert 'http' not in str(response.data)
        customer = emoji_customer.get(phone_number)
        assert 'stop' in customer
        assert customer['stop'] is not None

    def test_dashboard_unreachable(self):
        Config.DASHBOARD_ENABLED = False
        response = self.app.get("/corgi/all")
        assert '/corgi/all' not in str(response.data)
        assert 'table' not in str(response.data)

    def test_dashboard_reachable(self):
        Config.DASHBOARD_ENABLED = True
        response = self.app.get("/corgi/all")
        assert 'table' in str(response.data)

        # We should have rows.  And images.
        assert '<tr' in str(response.data)
        assert '<img' in str(response.data)


def string_contains_image(image_string):
    return (
        '.jpg' in str(image_string) or
        '.gif' in str(image_string) or
        '.png' in str(image_string) or
        'gstatic.com' in str(image_string)
    )

if __name__ == '__main__':
    unittest.main()
