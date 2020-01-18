# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the monitoring app of the travel_budgeter project."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def monitoring(request):
    """
    View to the monitoring page.
    """
    context = {}
    return render(request, "monitoring.html", context)
