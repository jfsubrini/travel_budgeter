# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Wallet forms, to save the travel user wallets and transactions types."""


from django.forms import ModelForm
from .models import Wallet, Transaction


class WalletForm(ModelForm):
    """Form to create the wallet data."""

    class Meta:
        """Details of the WalletForm form."""

        model = Wallet
        fields = "__all__"


class TransactionForm(ModelForm):
    """Form to create the transaction type data."""

    class Meta:
        """Details of the TransactionForm form."""

        model = Transaction
        fields = "__all__"
