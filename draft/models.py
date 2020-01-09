# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the draft app of the travel_budgeter project."""

from django.conf import settings
from django.db import models


class Draft(models.Model):
    """
    To create the Draft table in the database.
    """

    destination = models.CharField(
        "Nom du pays ou territoire", max_length=50, unique=True
    )
    currency = models.CharField("Devise", max_length=3)
    departure_date = models.DateField("Date de départ")
    travel_duration = models.PositiveSmallIntegerField("Durée du voyage (en jours)")
    pre_departure = models.PositiveSmallIntegerField("Dépenses avant le départ")
    international_transport = models.PositiveSmallIntegerField(
        "Transports internationaux"
    )
    local_transport = models.PositiveSmallIntegerField("Transports nationaux")
    lodging = models.PositiveSmallIntegerField("Hébergements")
    fooding = models.PositiveSmallIntegerField("Nourriture")
    visiting = models.PositiveSmallIntegerField("Visites")
    activities = models.PositiveSmallIntegerField("Activités")
    souvenirs = models.PositiveSmallIntegerField("Souvenirs")
    various = models.PositiveSmallIntegerField("Divers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drafts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Budget prévisionnel"

    def __str__(self):
        return f"Budget prévisionnel pour la destination : {self.destination}"
