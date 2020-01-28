# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,no-member
"""Creation of the Draft form, to define the travel budget goal of the user."""


from django.forms import DateInput, ModelForm, Form, Select, ModelChoiceField
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


# Select Draft form.
class SelectDraftForm(Form):
    """Form to select the saved travel user draft(s)."""

    def __init__(self, user, *args, **kwargs):
        # To display the drafts choices : only the one(s) of the travel user logged.
        super().__init__(*args, **kwargs)
        self.fields["select_draft"].queryset = Draft.objects.filter(user=user)

    select_draft = ModelChoiceField(queryset=None, widget=Select, required=True)
