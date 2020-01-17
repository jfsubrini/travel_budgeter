# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Expenses form, to save the travel user expenses,
before and during his journey."""


from django.forms import DateInput, ModelForm
from .models import Expense


class DateInputNicer(DateInput):
    """A widget which displays a better DateInput interface to place a date."""

    input_type = "date"


class ExpenseForm(ModelForm):
    """Form to create the expense data."""

    class Meta:
        """Details of the ExpenseForm form."""

        model = Expense
        fields = "__all__"
        widgets = {"date": DateInputNicer()}
