from django.test import TransactionTestCase
from .models import Transaction
from decimal import Decimal
from unittest.mock import patch
import requests


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


def mock_fixer_response(*args, **kwargs):
    return MockResponse()


class TestModels(TransactionTestCase):
    def testCreateTransaction(self):
        transaction = Transaction.activetransactions.create(
            label='test',
            initial_amount=123.45,
            initial_currency = 'EUR'
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
                initial_currency='USD'
            )
        self.assertEqual('test', transaction.label)
        self.assertEqual(123.45, transaction.initial_amount)
        self.assertEqual(105.91111873713109, transaction.converted_amount)
        self.assertEqual(1.1656, transaction.conversion_rate)

        t2 = Transaction.activetransactions.get(pk=transaction.id)
        self.assertEqual('test', t2.label)
        self.assertEqual(Decimal('123.45'), t2.initial_amount)
        self.assertEqual(Decimal('105.91'), t2.converted_amount)
        self.assertEqual(Decimal('1.165612312340666603720139741'), t2.conversion_rate)

    def testZeroAmount(self):
        transaction = Transaction.activetransactions.create(
            label='test',
            initial_amount=0,
        )
        with self.assertRaises(Exception):
            transaction.conversion_rate

