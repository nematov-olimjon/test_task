from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, **kwargs):
    wallet = instance.wallet

    for t in wallet.transactions.all():
        wallet.balance += t.amount
    wallet.save()
