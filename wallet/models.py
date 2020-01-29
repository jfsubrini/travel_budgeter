# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods,unnecessary-comprehension
"""All the models for the wallet app of the travel_budgeter project."""

from django.db import models
from draft.models import Draft
from xconverter.models import Currency


PAYMENT_TYPE = [
    "Carte bancaire Visa",
    "Carte bancaire MasterCard",
    "Porte-monnaie",
    "Chèque de voyage",
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
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name="Devise"
    )
    balance = models.PositiveIntegerField("Solde")
    draft = models.ForeignKey(
        Draft,
        on_delete=models.CASCADE,
        related_name="wallets",
        verbose_name="budget prévisionnel",
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portefeuille"

    def __str__(self):
        payment_type_name = PAYMENT_TYPE[int(self.payment_type) - 1]
        return f"{payment_type_name} du compte {self.wallet_name} en {self.currency}"


class Withdrawal(models.Model):
    """To create the Withdrawal table in the database."""

    PAYMENT_TYPE_CHOICES = [(i, money) for i, money in enumerate(PAYMENT_TYPE, start=1)]

    bank = models.CharField(
        "Nom de la banque de retrait", max_length=30, blank=True, null=True
    )
    country = models.CharField("Pays", max_length=70, blank=True, null=True)
    place = models.CharField("Lieu", max_length=70, blank=True, null=True)
    payment_type_out = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        related_name="credit_card_withdrawals",
        verbose_name="Carte bancaire débitée",
    )
    amount = models.PositiveIntegerField("Montant")
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name="Devise"
    )
    rate = models.FloatField("Taux de change (si vous l'avez)", blank=True, null=True)
    date = models.DateField("Date")
    payment_type_in = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        related_name="withdrawals_to_wallet",
        verbose_name="Porte-monnaie crédité",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Retrait"

    def __str__(self):
        return f"Retrait avec {self.payment_type_out} en {self.currency}"


class Change(models.Model):
    """To create the Change table in the database."""

    PAYMENT_TYPE_CHOICES = [(i, money) for i, money in enumerate(PAYMENT_TYPE, start=1)]

    changer = models.CharField(
        "Banque ou changeur", max_length=30, blank=True, null=True
    )
    country = models.CharField("Pays", max_length=70, blank=True, null=True)
    place = models.CharField("Lieu", max_length=70, blank=True, null=True)
    payment_type_out = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        related_name="wallet_for_changes",
        verbose_name="Porte-monnaie de la devise à changer",
    )
    amount = models.PositiveIntegerField("Montant")
    currency_out = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="changes_currencies",
        verbose_name="Devise à changer",
    )
    currency_in = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="changed_currencies",
        verbose_name="Devise reçue",
    )
    rate = models.FloatField("Taux de change")
    date = models.DateField("Date")
    payment_type_in = models.ForeignKey(
        PaymentType,
        on_delete=models.CASCADE,
        related_name="changes_to_wallet",
        verbose_name="Porte-monnaie de la devise reçue",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Change de devises"

    def __str__(self):
        return f"Change avec {self.payment_type_out} de {self.currency_out} en {self.currency_in}"
