# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the wallet app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import WalletForm, TransactionForm


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def wallet(request):
    """
    View to the wallet page.
    """
    # Analysis and treatment of the wallet forms that have been sent.
    # When the form have been posted.
    if request.method == "POST":
        # Checking if the forms have been validated.
        wallet_form = WalletForm(request.POST)
        transaction_form = TransactionForm(request.POST)
        if wallet_form.is_valid() and transaction_form.is_valid():
            # Saving the data from the wallet forms to the database.
            form1 = wallet_form.save(commit=False)
            form2 = transaction_form.save(commit=False)
            # Link the instance with a specific draft
            # (the one that this transaction has to be related).
            # travel_user = User.objects.get(
            #     username=request.user.username, password=request.user.password
            # )
            # form.user = travel_user
            # # Saving the categories data.
            # form2.save()
            # # Link the travel data with the right categories data (the last saved).
            # draft_category = Category.objects.last()
            # form1.category = draft_category
            # form1.save()
            # Redirecting to the expenses page.
            return redirect(f"/monitoring?user={request.user.id}")

    # To display the empty wallet forms.
    else:
        wallet_form = WalletForm()
        transaction_form = TransactionForm()

    # What to render to the template.
    context = {"wallet_form": wallet_form, "transaction_form": transaction_form}

    return render(request, "wallet.html", context)
