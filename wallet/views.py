# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""All the views for the wallet app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import WalletCreationForm


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def wallet_creation(request):
    """
    View to the wallet creation page.
    """
    # Analysis and treatment of the wallet form that has been sent.
    # When the form has been posted.
    if request.method == "POST":
        # Checking if the form has been validated.
        wallet_form = WalletCreationForm(request.POST)
        if wallet_form.is_valid():
            # Saving the data from the wallet form to the database.
            wallet_form.save()
            # Redirecting to the monitoring page.
            return redirect(f"/monitoring?user={request.user.id}")

    # To display the empty wallet form.
    else:
        wallet_form = WalletCreationForm()

    # What to render to the template.
    context = {"wallet_form": wallet_form}

    return render(request, "wallet.html", context)
