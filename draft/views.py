# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the draft app of the travel_budgeter project."""

from django.shortcuts import render


def draft(request):
    """
    View to the draft page.
    """
    context = {}
    return render(request, "draft.html", context)
