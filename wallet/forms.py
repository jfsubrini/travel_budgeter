# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Wallet forms, to save the travel user wallets and transactions types."""


from django.forms import ModelForm
from .models import Wallet


class WalletCreationForm(ModelForm):
    """Form to create the wallet data."""

    class Meta:
        """Details of the WalletCreationForm form."""

        model = Wallet
        exclude = ["draft"]
