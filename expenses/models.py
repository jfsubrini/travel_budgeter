# -*- coding: utf-8 -*-
# pylint: disable=
"""All the models for the expenses app of the travel_budgeter project."""

from django.db import models

from draft.models import TravelUser


class Expenses(models.Model):
    """To create the Expenses table."""

    label = models.CharField("Intitulé de la dépense", max_length=150)
    currency = models.CharField("Devise", max_length=3)
    amount = models.PositiveSmallIntegerField("Montant")
    travel_user = models.ForeignKey(
        TravelUser,
        on_delete=models.CASCADE,
        related_name="user_expenses",
        verbose_name="dépenses de l'utilisateur",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "pays ou territoire"

    def __str__(self):
        return self.label


class Category(models.Model):
    """To create the Category table."""

    name = models.CharField("Nom de la catégorie", max_length=50)
    expense = models.ForeignKey(
        Expenses,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="....",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "....."

    def __str__(self):
        return self.name
