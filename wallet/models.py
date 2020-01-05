# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the wallet app of the travel_budgeter project."""

from django.db import models


class Wallet(models.Model):
    """
    To create the Wallet table in the database.
    """

    first_name = models.CharField("prénom", max_length=50)
    last_name = models.CharField("nom", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "portefeuille"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
