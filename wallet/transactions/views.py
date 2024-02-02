from rest_framework import viewsets, filters
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['label']
    ordering_fields = ['balance', 'label']


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['txid']
    ordering_fields = ['amount', 'txid']
