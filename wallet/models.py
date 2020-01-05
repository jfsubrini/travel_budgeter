# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the wallet app of the travel_budgeter project."""

from django.db import models

WALLET_TYPE = ["....", "....", "....", "...."]


class Wallet(models.Model):
    """
    To create the Wallet table in the database.
    """

    WALLET_CHOICES = [(i, wallet) for i, wallet in enumerate(WALLET_TYPE, start=1)]

    wallet_type = models.PositiveSmallIntegerField(
        "Type de portefeuille", choices=WALLET_CHOICES
    )
    currency = models.CharField("Devise", max_length=3)
    amount = models.PositiveSmallIntegerField("Montant")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portefeuille"

    def __str__(self):
        return self.wallet_type
