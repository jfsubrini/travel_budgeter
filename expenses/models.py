# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the expenses app of the travel_budgeter project."""

from django.conf import settings
from django.db import models

from draft.models import TravelUser
from wallet.models import Wallet


class Expenses(models.Model):
    """To create the Expenses table."""

    label = models.CharField("Intitulé de la dépense", max_length=150)
    country = models.CharField("Pays", max_length=50)
    place = models.CharField("Endroit", max_length=100, blank=True, null=True)
    currency = models.CharField("Devise", max_length=3)
    amount = models.PositiveSmallIntegerField("Montant")
    date = models.DateField("Date")
    photo = models.ImageField(
        "Photo de la facture", upload_to="expenses/", blank=True, null=True
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="....",  # TODO
        verbose_name="....",  # TODO
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drafts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dépenses"

    def __str__(self):
        return self.label


class Category(models.Model):  # TODO
    """To create the Category table."""

    name = models.CharField("Nom de la catégorie", max_length=50)
    expense = models.ForeignKey(
        Expenses,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="....",  # TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "....."  # TODO

    def __str__(self):
        return self.name
