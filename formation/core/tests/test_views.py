from django.test import TransactionTestCase
from core.models import Transaction
from django.urls import reverse


class TestViews(TransactionTestCase):
    def setUp(self):
        self.transaction1 = Transaction.objects.create(
            label="Transaction 1",
            initial_amount=12.34,
        )

    def testTransactionList(self):
        response = self.client.get(
            reverse('transaction_list')
        )
        self.assertEqual(200, response.status_code)

    def testTransactionDetailOK(self):
        response = self.client.get(
            reverse(
                'transaction_detail',
                args=(
                    self.transaction1.id,
                ),
            )
        )
        self.assertEqual(200, response.status_code)

    def testTransactionDetailKO(self):
        response = self.client.get(
            reverse(
                'transaction_detail',
                args=(
                    99999,
                ),
            )
        )
        self.assertEqual(404, response.status_code)
