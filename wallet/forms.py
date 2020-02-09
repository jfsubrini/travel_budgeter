# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,no-member
"""Creation of the Wallet forms, to save the travel user wallets,
withdrawals and currency exchange data."""


from django.forms import DateInput, ModelForm, Form, ModelChoiceField, Select
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

    def __init__(self, last_draft, *args, **kwargs):
        # To filter the wallet choices : for 'Carte bancaire débitée', only credit card(s)
        # of the travel user logged and the one(s) created for the current draft.
        # For 'Porte-monnaie crédité', idem but only wallet(s).
        super().__init__(*args, **kwargs)
        self.fields["payment_type_out"].queryset = PaymentType.objects.filter(
            draft=last_draft, payment_type__lte=2
        )
        self.fields["payment_type_in"].queryset = PaymentType.objects.filter(
            draft=last_draft, payment_type=3
        )


class WalletChangeForm(ModelForm):
    """Form to enter the currency change data."""

    class Meta:
        """Details of the WalletChangeForm form."""

        model = Change
        fields = "__all__"
        widgets = {"date": DateInputNicer()}

    def __init__(self, last_draft, *args, **kwargs):
        # To filter the wallet choices : only wallet(s) of the travel user logged
        # and the one(s) created for the current draft.
        super().__init__(*args, **kwargs)
        self.fields["payment_type_out"].queryset = PaymentType.objects.filter(
            draft=last_draft, payment_type=3
        )
        self.fields["payment_type_in"].queryset = PaymentType.objects.filter(
            draft=last_draft, payment_type=3
        )


# Select Wallet form.
class SelectWalletForm(Form):
    """Form to select the saved travel user wallet(s)."""

    def __init__(self, draft, *args, **kwargs):
        # To display the wallets choices : only the one(s) of the travel user logged.
        super().__init__(*args, **kwargs)
        self.fields["select_wallet"].queryset = PaymentType.objects.filter(draft=draft)

    select_wallet = ModelChoiceField(
        label="Vos 'wallets' :", queryset=None, widget=Select, required=True
    )


# Edit Wallet form.
class EditWalletForm(ModelForm):
    """Form to edit the selected wallet the travel user wants to modify."""

    class Meta:
        """Details of the EditWalletForm form."""

        model = PaymentType
        exclude = ["draft"]

    def __init__(self, instance, *args, **kwargs):
        # To display the instance data as default values for the selected wallet.
        super().__init__(*args, **kwargs)
        self.fields["wallet_name"].initial = instance.wallet_name
        self.fields["payment_type"].initial = instance.payment_type
        self.fields["currency"].initial = instance.currency
        self.fields["balance"].initial = instance.balance
