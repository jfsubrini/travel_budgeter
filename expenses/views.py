# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the expenses app of the travel_budgeter project."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def expenses(request):
    """
    View to the expenses page.
    """
    context = {}
    return render(request, "expenses.html", context)
