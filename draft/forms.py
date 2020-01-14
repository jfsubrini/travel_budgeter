# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Draft form, to define the travel budget goal of the user."""


from django.forms import DateInput, ModelForm
from .models import Category, Draft


class DateInputNicer(DateInput):
    """A widget which displays a better DateInput interface to place a date."""

    input_type = "date"


# Draft forms.
class DraftForm(ModelForm):
    """Form to create the travel budget main data."""

    class Meta:
        """Details of the DraftForm form."""

        model = Draft
        exclude = ["user", "category"]
        widgets = {"departure_date": DateInputNicer()}


class DraftForm2(ModelForm):
    """Form to create the travel budget goal per category."""

    class Meta:
        """Details of the DraftForm2 form."""

        model = Category
        fields = "__all__"
