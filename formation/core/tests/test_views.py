from django.test import TransactionTestCase
from core.models import Transaction
from django.contrib.auth.models import User
from django.urls import reverse


class TestViews(TransactionTestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            'Test User',
            'test@test.com',
            'password',
        )
        self.transaction1 = Transaction.objects.create(
            label="Transaction 1",
            initial_amount=12.34,
            owner=self.user1,
        )

    def testTransactionList(self):
        response = self.client.get(
            reverse('transaction_list')
        )
        self.assertEqual(200, response.status_code)

    def testTransactionDetailOK(self):
        self.client.force_login(self.user1)
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
