# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,no-member
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

    def __init__(self, user, *args, **kwargs):
        # To filter the wallet choices : for 'Carte bancaire débitée', only credit card(s)
        # of the travel user logged and the one(s) created for the current draft.
        # For 'Porte-monnaie crédité', idem but only wallet(s).
        super().__init__(*args, **kwargs)
        self.fields["payment_type_out"].queryset = PaymentType.objects.filter(
            draft__user=user, payment_type__lte=2
        )
        self.fields["payment_type_in"].queryset = PaymentType.objects.filter(
            draft__user=user, payment_type=3
        )


class WalletChangeForm(ModelForm):
    """Form to enter the currency change data."""

    class Meta:
        """Details of the WalletChangeForm form."""

        model = Change
        fields = "__all__"
        widgets = {"date": DateInputNicer()}

    def __init__(self, user, *args, **kwargs):
        # To filter the wallet choices : only wallet(s) of the travel user logged
        # and the one(s) created for the current draft.
        super().__init__(*args, **kwargs)
        self.fields["payment_type_out"].queryset = PaymentType.objects.filter(
            draft__user=user, payment_type=3
        )
        self.fields["payment_type_in"].queryset = PaymentType.objects.filter(
            draft__user=user, payment_type=3
        )
