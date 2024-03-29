# -*- coding: utf-8 -*-
# pylint: disable=invalid-name,missing-class-docstring,missing-module-docstring
# Generated by Django 2.2.5 on 2020-01-30 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pre_departure",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Dépenses avant le départ"
                    ),
                ),
                (
                    "international_transport",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Transports internationaux"
                    ),
                ),
                (
                    "local_transport",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Transports nationaux"
                    ),
                ),
                (
                    "lodging",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Hébergements"
                    ),
                ),
                (
                    "fooding",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Nourriture"
                    ),
                ),
                (
                    "visiting",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Visites"
                    ),
                ),
                (
                    "activities",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Activités"
                    ),
                ),
                (
                    "souvenirs",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Souvenirs"
                    ),
                ),
                (
                    "various",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Divers"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Catégorie"},
        ),
        migrations.CreateModel(
            name="Draft",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "destination",
                    models.CharField(
                        max_length=70, verbose_name="Nom de la destination de voyage"
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("EUR", "EUR"),
                            ("USD", "USD"),
                            ("GBP", "GBP"),
                            ("CAD", "CAD"),
                            ("CHF", "CHF"),
                            ("AUD", "AUD"),
                        ],
                        max_length=3,
                        verbose_name="Devise",
                    ),
                ),
                (
                    "departure_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Date de départ en voyage"
                    ),
                ),
                (
                    "travel_duration",
                    models.PositiveSmallIntegerField(
                        verbose_name="Durée du voyage (en jours)"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="draft.Category",
                        verbose_name="Catégorie",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="drafts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "Budget prévisionnel"},
        ),
    ]
