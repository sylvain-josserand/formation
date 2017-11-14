from django.test import TransactionTestCase
from .models import Transaction
from decimal import Decimal


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
