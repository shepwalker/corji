# This Python file uses the following encoding: utf-8
import random
import unittest

from corji.models import emoji_customer


# TODO: actually relying on the SPREADSHEET_URL is a codesmell.
class CustomerDataTestCase(unittest.TestCase):

    def test_sanity(self):
        assert True

    def test_get_if_not_exists_should_return_none(self):
        customer = emoji_customer.get(str(random.random()))
        assert customer is None

    def test_get_base_case(self):
        phone_number = "Hiya"

        customer = emoji_customer.get(phone_number)
        assert customer is not None
        assert customer['phone_number']['S'] == phone_number

    def test_new_customer(self):
        phone_number = str(random.random())

        assert emoji_customer.get(phone_number) is None

        emoji_customer.new(phone_number)
        assert emoji_customer.get(phone_number) is not None

    def test_add_metadata(self):
        phone_number = "Hiya"
        metadata = str(random.random())

        assert metadata not in emoji_customer.get(phone_number)

        emoji_customer.add_metadata(phone_number, metadata, "whatever")

        customer = emoji_customer.get(phone_number)
        assert metadata in customer
        assert customer[metadata]['S'] == 'whatever'

    def test_modify_consumptions(self):
        phone_number = "Hiya"

        customer = emoji_customer.get(phone_number)
        first_consumptions = int(customer['consumptions']['N'])

        emoji_customer.modify_consumptions(phone_number, consumptions=-10)

        customer = emoji_customer.get(phone_number)
        second_consumptions = int(customer['consumptions']['N'])

        assert first_consumptions + 10 == second_consumptions
