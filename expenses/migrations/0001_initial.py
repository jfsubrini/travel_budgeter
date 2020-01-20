# -*- coding: utf-8 -*-
# pylint: disable=invalid-name,missing-class-docstring,missing-module-docstring
# Generated by Django 2.2.5 on 2020-01-20 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wallet", "0001_initial"),
        ("xconverter", "0002_auto_20200114_1302"),
        ("draft", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
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
                    "label",
                    models.CharField(
                        max_length=200, verbose_name="Intitulé de la dépense"
                    ),
                ),
                ("country", models.CharField(max_length=70, verbose_name="Pays")),
                (
                    "place",
                    models.CharField(
                        blank=True, max_length=70, null=True, verbose_name="Endroit"
                    ),
                ),
                ("date", models.DateField(verbose_name="Date")),
                (
                    "category",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Dépenses avant le départ"),
                            (2, "Transport international"),
                            (3, "Transport local"),
                            (4, "Hébergement"),
                            (5, "Nourriture"),
                            (6, "Visites"),
                            (7, "Activités"),
                            (8, "Souvenirs"),
                            (9, "Divers"),
                        ],
                        verbose_name="catégorie",
                    ),
                ),
                ("amount", models.PositiveSmallIntegerField(verbose_name="Montant")),
                (
                    "simulation",
                    models.BooleanField(default=False, verbose_name="Simulation"),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="expenses/",
                        verbose_name="Photo de la facture",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="xconverter.Currency",
                        verbose_name="monnaie",
                    ),
                ),
                (
                    "draft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expenses",
                        to="draft.Draft",
                        verbose_name="budget prévisionnel",
                    ),
                ),
                (
                    "payment_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wallet.PaymentType",
                        verbose_name="type de paiement",
                    ),
                ),
            ],
            options={"verbose_name": "Dépenses"},
        )
    ]
