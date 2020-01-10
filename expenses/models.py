# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the expenses app of the travel_budgeter project."""

from django.conf import settings
from django.db import models

from draft.models import Draft
from wallet.models import Wallet


class Expense(models.Model):
    """To create the Expense table."""

    label = models.CharField("Intitulé de la dépense", max_length=200)
    country = models.CharField("Pays", max_length=70)
    place = models.CharField("Endroit", max_length=70, blank=True, null=True)
    currency = models.CharField("Devise", max_length=3)
    amount = models.PositiveSmallIntegerField("Montant")
    date = models.DateField("Date")
    photo = models.ImageField(
        "Photo de la facture", upload_to="expenses/", blank=True, null=True
    )
    simulation = models.BooleanField("Simulation", default=False)
    draft = models.ForeignKey(
        Draft,
        on_delete=models.CASCADE,
        related_name="....",  # TODO
        verbose_name="....",  # TODO
    )
    category = models.ForeignKey(
        Draft,
        on_delete=models.CASCADE,
        related_name="....",  # TODO
        verbose_name="....",  # TODO
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="....",  # TODO
        verbose_name="....",  # TODO
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drafts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dépenses"

    def __str__(self):
        return self.label
