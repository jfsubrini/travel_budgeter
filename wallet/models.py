# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the wallet app of the travel_budgeter project."""

from django.conf import settings
from django.db import models


MONEY_TYPE = ["Carte bancaire Visa", "Carte bancaire MasterCard", "Porte-monnaie"]
TRANSACTION = [
    "Paiement carte bancaire",
    "Retrait ATM",
    "Retrait GAB",
    "Virement bancaire",
    "Paiement Paypal, ApplePay, etc.",
    "Crédit",
]
CURRENCY = ["EUR", "USD", "GBP", "CAD", "CHF", "AUD"]


class Wallet(models.Model):
    """
    To create the Wallet table in the database.
    """

    MONEY_TYPE_CHOICES = [(i, money) for i, money in enumerate(MONEY_TYPE, start=1)]
    CURRENCY_CHOICES = [(i, curr) for i, curr in enumerate(CURRENCY, start=1)]

    name = models.CharField("Nom du portefeuille", max_length=30)
    money_type = models.PositiveSmallIntegerField(
        "Type de portefeuille", choices=MONEY_TYPE_CHOICES
    )
    currency = models.CharField("Devise", max_length=3, choices=CURRENCY_CHOICES)
    balance = models.PositiveSmallIntegerField("Solde")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portefeuille"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    To create the Transaction table in the database.
    """

    TRANSACTION_CHOICES = [(i, trans) for i, trans in enumerate(TRANSACTION, start=1)]

    type_ = models.PositiveSmallIntegerField(
        "Type de transaction", choices=TRANSACTION_CHOICES
    )
    rate = models.FloatField("Taux de change")
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="....",  # TODO
        verbose_name="....",  # TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transaction"

    def __str__(self):
        return self.type_
