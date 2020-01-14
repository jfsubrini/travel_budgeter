# -*- coding: utf-8 -*-
# pylint: disable=
"""Creation of the Draft form, to define the travel budget goal of the user."""


from django.forms import (
    CheckboxSelectMultiple,
    DateInput,
    EmailInput,
    ModelForm,
    NullBooleanSelect,
    PasswordInput,
    RadioSelect,
    Select,
    TextInput,
    MultipleChoiceField,
    Form,
)
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
        exclude = ["user"]
        widgets = {"departure_date": DateInputNicer()}


class DraftForm2(Form):
    """Form to create the travel budget goal per category."""

    class Meta:
        """Details of the DraftForm2 form."""

        model = Category
        fields = "__all__"
        widgets = {}
