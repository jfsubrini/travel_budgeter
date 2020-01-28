# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Creation of the Simulations Deletion form,
to be able to delete all the simulations from one draft."""


from django.forms import Form, ChoiceField, RadioSelect


class SimulationsDeletionForm(Form):
    """Form to delete all the simulations."""

    CHOICES = [("1", "Oui"), ("2", "Non")]

    radio_deletion = ChoiceField(
        widget=RadioSelect,
        label="Suppression de toutes les simulations ?",
        choices=CHOICES,
    )
