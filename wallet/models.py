# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods,unnecessary-comprehension
"""All the models for the wallet app of the travel_budgeter project."""

from django.db import models
from draft.models import Draft
from xconverter.models import Currency


PAYMENT_TYPE = [
    "Achat par carte bancaire Visa",
    "Achat par carte bancaire MasterCard",
    "Paiement en liquide avec le porte-monnaie",
    "Paiement par chèque de voyage",
    "Paiement ou virement d'un compte Paypal, ApplePay, bancaire, etc.",
]
CURRENCY = (
    ("EUR", "EUR"),
    ("USD", "USD"),
    ("GBP", "GBP"),
    ("CAD", "CAD"),
    ("CHF", "CHF"),
    ("AUD", "AUD"),
)


class PaymentType(models.Model):
    """To create the PaymentType table in the database."""

    PAYMENT_TYPE_CHOICES = [(i, money) for i, money in enumerate(PAYMENT_TYPE, start=1)]

    wallet_name = models.CharField("Nom du portefeuille", max_length=30)
    payment_type = models.PositiveSmallIntegerField(
        "Type de portefeuille", choices=PAYMENT_TYPE_CHOICES
    )
    currency = models.CharField("Devise", max_length=3, choices=CURRENCY)
    balance = models.PositiveSmallIntegerField("Solde")
    draft = models.ForeignKey(
        Draft,
        on_delete=models.CASCADE,
        related_name="wallets",
        verbose_name="budget prévisionnel",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portefeuille"

    def __str__(self):
        payment_type_name = PAYMENT_TYPE[int(self.payment_type) - 1]
        return f"Wallet {self.wallet_name} : {payment_type_name} en {self.currency}"


class Withdrawal(models.Model):
    """To create the Withdrawal table in the database."""

    PAYMENT_TYPE_CHOICES = [
        (i, money) for i, money in enumerate(PAYMENT_TYPE, start=1)
    ]  # TODO

    bank = models.CharField(
        "Nom de la banque de retrait", max_length=30, blank=True, null=True
    )
    country = models.CharField("Pays", max_length=70, blank=True, null=True)
    place = models.CharField("Lieu", max_length=70, blank=True, null=True)
    payment_type_out = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE, verbose_name="Carte bancaire débitée"
    )  # TODO
    amount = models.PositiveSmallIntegerField("Montant")
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name="Monnaie"
    )
    rate = models.FloatField("Taux de change (si vous l'avez)", blank=True, null=True)
    date = models.DateField("Date")
    payment_type_in = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE, verbose_name="Porte-monnaie crédité"
    )  # TODO
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Retrait"

    def __str__(self):
        payment_type_name = PAYMENT_TYPE[int(self.payment_type_out) - 1]  # TODO
        return f"Retrait avec {payment_type_name} en {self.currency}"
