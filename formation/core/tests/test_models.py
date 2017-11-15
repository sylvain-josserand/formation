from django.contrib.auth.models import User
from django.test import TransactionTestCase
from core.models import Transaction
from decimal import Decimal
from unittest.mock import patch


class MockResponse:
    status_code = 200

    def json(self):
        return {
            "base": "EUR",
            "date": "2017-11-13",
            "rates": {
                "USD": 1.1656,
            }
        }


class MockBadResponse:
    status_code = 501


def mock_fixer_response(*args, **kwargs):
    return MockResponse()


def mock_fixer_bad_response(*args, **kwargs):
    return MockBadResponse()



class TestModels(TransactionTestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('Test User')
    def testCreateTransaction(self):
        transaction = Transaction.activetransactions.create(
            label='test',
            initial_amount=123.45,
            initial_currency = 'EUR',
            owner=self.user1,
        )
        self.assertEqual('test', transaction.label)
        self.assertEqual(123.45, transaction.initial_amount)
        self.assertEqual(123.45, transaction.converted_amount)
        self.assertEqual(1, transaction.conversion_rate)

        t2 = Transaction.activetransactions.get(pk=transaction.id)
        self.assertEqual('test', t2.label)
        self.assertEqual(Decimal('123.45'), t2.initial_amount)
        self.assertEqual(Decimal('123.45'), t2.converted_amount)
        self.assertEqual(1, t2.conversion_rate)

    def testConvertCurrency(self):
        with patch('requests.get', mock_fixer_response) as mock_request:
            transaction = Transaction.activetransactions.create(
                label='test',
                initial_amount=123.45,
                initial_currency='USD',
                owner=self.user1,
            )
        self.assertEqual('test', transaction.label)
        self.assertEqual(123.45, transaction.initial_amount)
        self.assertEqual(Decimal('105.9111187371310964980345860'), transaction.converted_amount)
        self.assertEqual(Decimal('1.165599999999999969446662362'), transaction.conversion_rate)

        t2 = Transaction.activetransactions.get(pk=transaction.id)
        self.assertEqual('test', t2.label)
        self.assertEqual(Decimal('123.45'), t2.initial_amount)
        self.assertEqual(Decimal('105.91'), t2.converted_amount)
        self.assertEqual(Decimal('1.165612312340666603720139741'), t2.conversion_rate)

    def testZeroAmount(self):
        transaction = Transaction.activetransactions.create(
            label='test',
            initial_amount=0,
            owner=self.user1,
        )
        with self.assertRaises(Exception):
            transaction.conversion_rate

    def testResonseCode(self):
        with self.assertRaises(Exception):
            with patch('requests.get', mock_fixer_bad_response) as mock_request:
                transaction = Transaction.activetransactions.create(
                    label='test1',
                    initial_amount=123.45,
                    initial_currency='USD',
                    owner=self.user1,
                )