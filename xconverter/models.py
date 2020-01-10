# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the xconverter app of the travel_budgeter project."""

from django.db import models


class Currency(models.Model):
    """To create the Currency table."""

    country = models.CharField("Pays", max_length=70)
    name = models.CharField("Devise", max_length=70)
    iso = models.CharField("ISO", max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dépenses"

    def __str__(self):
        return self.country
