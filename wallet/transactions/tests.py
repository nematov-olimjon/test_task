from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Wallet, Transaction
import logging
logger = logging.getLogger(__name__)



class WalletViewSetTestCase(APITestCase):
    def setUp(self):
        Wallet.objects.create(label='Wallet One', balance=100)
        Wallet.objects.create(label='Wallet Two', balance=200)
        Wallet.objects.create(label='Wallet Three', balance=300)

    def test_pagination(self):
        url = reverse('wallet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_filtering(self):
        url = reverse('wallet-list') + '?search=One'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['label'], 'Wallet One')

    def test_ordering(self):
        url = reverse('wallet-list') + '?ordering=balance'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], 'Wallet One')


class TransactionViewSetTestCase(APITestCase):
    def setUp(self):
        wallet = Wallet.objects.create(label='Test Wallet', balance=100)
        Transaction.objects.create(wallet=wallet, txid='TXID123', amount=10)
        Transaction.objects.create(wallet=wallet, txid='TXID456', amount=20)
        Transaction.objects.create(wallet=wallet, txid='TXID789', amount=30)

    def test_pagination(self):
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_filtering(self):
        url = reverse('transaction-list') + '?search=TXID123'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['txid'], 'TXID123')

    def test_ordering(self):
        url = reverse('transaction-list') + '?ordering=-amount'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['txid'], 'TXID789')
