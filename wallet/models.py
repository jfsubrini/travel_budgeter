# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods,unnecessary-comprehension
"""All the models for the wallet app of the travel_budgeter project."""

from django.db import models
from draft.models import Draft


MONEY_TYPE = [
    "Carte bancaire Visa (compte rattaché)",
    "Carte bancaire MasterCard (compte rattaché)",
    "Porte-monnaie",
    "Chèque de voyage",
    "Virement bancaire",
    "Compte Paypal, ApplePay, etc.",
]
TRANSACTION_TYPE = [
    "Retrait ATM",
    "Retrait DAB",
    "Achat par carte bancaire",
    "Virement bancaire",
    "Paiement en liquide",
    "Paiement Paypal, ApplePay, etc.",
    "Crédit sur un compte",
]
CURRENCY = (
    ("EUR", "EUR"),
    ("USD", "USD"),
    ("GBP", "GBP"),
    ("CAD", "CAD"),
    ("CHF", "CHF"),
    ("AUD", "AUD"),
)


class Wallet(models.Model):
    """To create the Wallet table in the database."""

    MONEY_TYPE_CHOICES = [(i, money) for i, money in enumerate(MONEY_TYPE, start=1)]

    name = models.CharField("Nom du portefeuille", max_length=30)
    money_type = models.PositiveSmallIntegerField(
        "Type de portefeuille", choices=MONEY_TYPE_CHOICES
    )
    currency = models.CharField("Devise", max_length=3, choices=CURRENCY)
    balance = models.PositiveSmallIntegerField("Solde")
    draft = models.ForeignKey(
        Draft,
        on_delete=models.CASCADE,
        related_name="wallets",
        verbose_name="budgets prévisionnels",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portefeuille"

    def __str__(self):
        money_type_name = MONEY_TYPE[int(self.money_type)]
        return f"Wallet {self.name} : {money_type_name} en {self.currency}"


class Transaction(models.Model):
    """To create the Transaction table in the database."""

    TRANSACTION_TYPE_CHOICES = [
        (i, trans) for i, trans in enumerate(TRANSACTION_TYPE, start=1)
    ]

    transaction_type = models.PositiveSmallIntegerField(
        "Type de transaction", choices=TRANSACTION_TYPE_CHOICES
    )
    rate = models.FloatField("Taux de change")
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, verbose_name="portefeuille"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transaction"

    def __str__(self):
        return self.transaction_type
