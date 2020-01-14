# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the expenses app of the travel_budgeter project."""

from django.shortcuts import render


def expenses(request):
    """
    View to the expenses page.
    """
    context = {}
    return render(request, "expenses.html", context)
