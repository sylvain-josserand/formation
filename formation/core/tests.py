from django.test import TransactionTestCase
from .models import Transaction
from decimal import Decimal


class TestModels(TransactionTestCase):
    def testCreateTransaction(self):
        transaction = Transaction.activetransactions.create(
            label='test',
            amount=123.45,
        )
        self.assertEqual('test', transaction.label)
        self.assertEqual(123.45, transaction.amount)

        t2 = Transaction.activetransactions.get(pk=transaction.id)
        self.assertEqual('test', t2.label)
        self.assertEqual(Decimal('123.45'), t2.amount)
