# -*- coding: utf-8 -*-
# pylint: disable=missing-class-docstring,too-few-public-methods
"""All the models for the draft app of the travel_budgeter project."""

from django.db import models


class TravelUser(models.Model):
    """
    To create the TravelUser table in the database.
    Gathering all the personnal data of the travel user.
    """

    first_name = models.CharField("Prénom", max_length=50)
    last_name = models.CharField("Nom", max_length=50)
    email = models.EmailField("Adresse email", max_length=100, unique=True)
    password = models.CharField("Mot de passe", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "utilisateur"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
    travel_user = models.ForeignKey(
        TravelUser,
        on_delete=models.CASCADE,
        related_name="drafts",
        verbose_name=".....",  # TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Budget prévisionnel"

    def __str__(self):
        return f"Budget prévisionnel pour la destination : {self.destination}"
