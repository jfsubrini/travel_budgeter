# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the wallet app of the travel_budgeter project."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def wallet(request):
    """
    View to the wallet page.
    """
    context = {}
    return render(request, "wallet.html", context)
