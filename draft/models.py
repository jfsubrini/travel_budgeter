# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the draft app of the travel_budgeter project."""

from django.conf import settings
from django.db import models


class Category(models.Model):
    """To create the Category table."""

    pre_departure = models.PositiveSmallIntegerField(
        "Dépenses avant le départ", blank=True, null=True
    )
    international_transport = models.PositiveSmallIntegerField(
        "Transports internationaux", blank=True, null=True
    )
    local_transport = models.PositiveSmallIntegerField(
        "Transports nationaux", blank=True, null=True
    )
    lodging = models.PositiveSmallIntegerField("Hébergements", blank=True, null=True)
    fooding = models.PositiveSmallIntegerField("Nourriture", blank=True, null=True)
    visiting = models.PositiveSmallIntegerField("Visites", blank=True, null=True)
    activities = models.PositiveSmallIntegerField("Activités", blank=True, null=True)
    souvenirs = models.PositiveSmallIntegerField("Souvenirs", blank=True, null=True)
    various = models.PositiveSmallIntegerField("Divers", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return "Catégorie"


class Draft(models.Model):
    """
    To create the Draft table in the database.
    """

    destination = models.CharField("Nom du pays ou territoire", max_length=70)
    currency = models.CharField("Devise", max_length=3)
    departure_date = models.DateField("Date de départ", blank=True, null=True)
    travel_duration = models.PositiveSmallIntegerField("Durée du voyage (en jours)")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drafts"
    )
    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, verbose_name="catégorie"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Budget prévisionnel"

    def __str__(self):
        return f"Budget prévisionnel pour la destination : {self.destination}"
