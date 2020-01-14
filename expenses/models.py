# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods,unnecessary-comprehension
"""All the models for the expenses app of the travel_budgeter project."""

from django.db import models

from draft.models import Draft
from wallet.models import Wallet
from xconverter.models import Currency


CATEGORY = [
    "Dépenses avant le départ",
    "Transport international",
    "Transport local",
    "Hébergement",
    "Nourriture",
    "Visites",
    "Activités",
    "Souvenirs",
    "Divers",
]


class Expense(models.Model):
    """To create the Expense table."""

    CATEGORY_CHOICES = [(i, cat) for i, cat in enumerate(CATEGORY, start=1)]

    label = models.CharField("Intitulé de la dépense", max_length=200)
    country = models.CharField("Pays", max_length=70)
    place = models.CharField("Endroit", max_length=70, blank=True, null=True)
    category = models.PositiveSmallIntegerField("catégorie", choices=CATEGORY_CHOICES)
    amount = models.PositiveSmallIntegerField("Montant")
    date = models.DateField("Date")
    photo = models.ImageField(
        "Photo de la facture", upload_to="expenses/", blank=True, null=True
    )
    simulation = models.BooleanField("Simulation", default=False)
    draft = models.ForeignKey(
        Draft, on_delete=models.CASCADE, verbose_name="budget prévisionnel"
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name="monnaie"
    )
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, verbose_name="portefeuille"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dépenses"

    def __str__(self):
        return self.label
