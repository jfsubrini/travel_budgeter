"""
Data migration, for the countries currencies, into the travelget postgreSQL database.
"""

import copy
import json
from django.db import migrations

from xconverter.migrations.tools.deserializer import load_json, json_to_model


def _populate_tables(choices, model_name, field):
    """Create all the choice names instances into the model table."""
    for choice, _ in choices:
        field_ = {}
        field_[field] = choice
        choice_name = model_name(**field_)
        choice_name.save()


def fill_currency(apps, _):
    """Filling the Currency table and other with the data by country."""
    # To get the historical version of the model using the app registry.
    Currency = apps.get_model("xconverter", "Currency")

    # Filling the Currency table.
    foreign_key_list = ["bad_climatic_season"]

    CURRENCY_DATA = load_json("territories_matrix/matrix/matrix_data.json")
    CURRENCY_DATA_FOR_COUNTRY = copy.deepcopy(CURRENCY_DATA)
    for territory in CURRENCY_DATA:
        for key in CURRENCY_DATA[territory]:
            if key in foreign_key_list:
                del CURRENCY_DATA_FOR_COUNTRY[territory][key]

    for territory in CURRENCY_DATA_FOR_COUNTRY:
        CURRENCY_DATA_JSON = json.dumps(MATRIX_DATA_FOR_TERRITORY[territory])
        json_to_model(CURRENCY_DATA_JSON, Currency)

    # Filling the other linked tables.
    # Create all the choice names instances into the model many to many tables.
    _populate_tables(MONTHS, BadClimaticSeason, "bad_climatic_season_month")

    # Populate each table with each territory instance.
    for territory in CURRENCY_DATA:
        value_name = CURRENCY_DATA[territory]["name"]

        # Filling the BadClimaticSeason table.
        filling_tables(
            key="bad_climatic_season",
            model_name=BadClimaticSeason,
            field="bad_climatic_season_month",
            key_territory=territory,
            rel_model_instance=Territory.objects.get(name=value_name),
            matrix=CURRENCY_DATA,
        )


def reverse_fill_currency(apps, _):
    """Reversed fill_currency function by deleting all the data."""
    # To get the historical version of the model using the app registry.
    Currency = apps.get_model("xconverter", "Currency")

    Currency.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [("xconverter", "0001_initial")]

    operations = [
        migrations.RunPython(fill_currency, reverse_code=reverse_fill_currency)
    ]
