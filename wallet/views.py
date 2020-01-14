# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the wallet app of the travel_budgeter project."""

from django.shortcuts import render


def wallet(request):
    """
    View to the wallet page.
    """
    context = {}
    return render(request, "wallet.html", context)
