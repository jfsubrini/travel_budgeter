# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the xconverter app of the travel_budgeter project."""

from django.shortcuts import render


def converter(request):
    """
    View to the converter page.
    """
    context = {}
    return render(request, "converter.html", context)
