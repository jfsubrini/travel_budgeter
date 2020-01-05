# -*- coding: utf-8 -*-
# pylint: disable=
"""All the models for the draft app of the travel_budgeter project."""

from django.db import models


class TravelUser(models.Model):
    """
    To create the TravelUser table in the database.
    Gathering all the personnal data of the travel user.
    """

    first_name = models.CharField("prénom", max_length=50)
    last_name = models.CharField("nom", max_length=50)
    email = models.EmailField("adresse email", max_length=100, unique=True)
    password = models.CharField("mot de passe", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "utilisateur"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
