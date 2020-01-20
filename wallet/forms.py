# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Wallet forms, to save the travel user wallets and transactions types."""


from django.forms import ModelForm
from .models import PaymentType


class WalletCreationForm(ModelForm):
    """Form to create the wallet data."""

    class Meta:
        """Details of the WalletCreationForm form."""

        model = PaymentType
        exclude = ["draft"]


class WalletWithdrawalForm(ModelForm):
    """Form to enter the credit card withdrawal data."""

    class Meta:
        """Details of the WalletWithdrawalForm form."""

        model = PaymentType
        exclude = ["draft"]


class WalletChangeForm(ModelForm):
    """Form to enter the currency change data."""

    class Meta:
        """Details of the WalletChangeForm form."""

        model = PaymentType
        exclude = ["draft"]
