# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Wallet forms, to save the travel user wallets,
withdrawals and currency exchange data."""


from django.forms import DateInput, ModelForm
from .models import Change, PaymentType, Withdrawal


class DateInputNicer(DateInput):
    """A widget which displays a better DateInput interface to place a date."""

    input_type = "date"


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

        model = Withdrawal
        fields = "__all__"
        widgets = {"date": DateInputNicer()}
        # TODO afficher les bons choix pour carte bancaire débitée et porte-monnaie crédité


class WalletChangeForm(ModelForm):
    """Form to enter the currency change data."""

    class Meta:
        """Details of the WalletChangeForm form."""

        model = Change
        fields = "__all__"
        widgets = {"date": DateInputNicer()}
        # TODO afficher les bons choix pour carte bancaire débitée et porte-monnaie crédité
