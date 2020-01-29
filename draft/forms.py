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


# Edit Draft forms.
class EditDraftForm(ModelForm):
    """Form to edit the selected draft the travel user wants to modify."""

    class Meta:
        """Details of the EditDraftForm form."""

        model = Draft
        exclude = ["user", "category"]
        widgets = {"departure_date": DateInput()}

    def __init__(self, instance, *args, **kwargs):
        # To display the instance data into the placeholder for the selected draft.
        super().__init__(*args, **kwargs)
        self.fields["destination"].widget.attrs["placeholder"] = instance.destination
        self.fields["currency"].widget.attrs["placeholder"] = instance.currency
        self.fields["departure_date"].widget.attrs[
            "placeholder"
        ] = instance.departure_date
        self.fields["travel_duration"].widget.attrs[
            "placeholder"
        ] = instance.travel_duration


class EditDraftForm2(ModelForm):
    """Form to edit the selected draft category values the travel user wants to modify."""

    class Meta:
        """Details of the EditDraftForm2 form."""

        model = Category
        fields = "__all__"

    def __init__(self, instance, *args, **kwargs):
        # To display the instance data into the placeholder for the selected draft.
        super().__init__(*args, **kwargs)
        self.fields["pre_departure"].widget.attrs[
            "placeholder"
        ] = instance.pre_departure
        self.fields["international_transport"].widget.attrs[
            "placeholder"
        ] = instance.international_transport
        self.fields["local_transport"].widget.attrs[
            "placeholder"
        ] = instance.local_transport
        self.fields["lodging"].widget.attrs["placeholder"] = instance.lodging
        self.fields["fooding"].widget.attrs["placeholder"] = instance.fooding
        self.fields["visiting"].widget.attrs["placeholder"] = instance.visiting
        self.fields["activities"].widget.attrs["placeholder"] = instance.activities
        self.fields["souvenirs"].widget.attrs["placeholder"] = instance.souvenirs
        self.fields["various"].widget.attrs["placeholder"] = instance.various
