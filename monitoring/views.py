# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the monitoring app of the travel_budgeter project."""

from django.shortcuts import render


def monitoring(request):
    """
    View to the monitoring page.
    """
    context = {}
    return render(request, "monitoring.html", context)
