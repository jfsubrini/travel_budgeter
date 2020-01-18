# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,no-member
"""Creation of the Expenses form, to save the travel user expenses,
before and during his journey."""


from django.forms import DateInput, ModelForm
from wallet.models import Wallet
from .models import Expense


class DateInputNicer(DateInput):
    """A widget which displays a better DateInput interface to place a date."""

    input_type = "date"


class ExpenseForm(ModelForm):
    """Form to create the expense data."""

    class Meta:
        """Details of the ExpenseForm form."""

        model = Expense
        exclude = ["draft"]
        widgets = {"date": DateInputNicer()}

    def __init__(self, user, *args, **kwargs):
        # To filter the wallet choices : only the one(s) of the travel user logged
        # and the one(s) created for the current draft.
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields["wallet"].queryset = Wallet.objects.filter(draft__user=user)
