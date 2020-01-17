# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Wallet forms, to save the travel user wallets and transactions types."""


from django.forms import ModelForm, Select
from .models import Wallet


class WalletCreationForm(ModelForm):
    """Form to create the wallet data."""

    class Meta:
        """Details of the WalletCreationForm form."""

        model = Wallet
        fields = "__all__"
        widgets = {"draft": Select()}
        # TODO pour la sélection des drafts ne doiventt apparaître
        # que ceux fait par le travel user logged.
