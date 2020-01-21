# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""All the views for the wallet app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from draft.models import Draft
from .forms import WalletCreationForm, WalletWithdrawalForm, WalletChangeForm


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
            # First, create, but don't save the new Wallet instance.
            form = wallet_form.save(commit=False)
            # Then, link the instance with the last draft from that logged travel user.
            last_draft = Draft.objects.filter(user=request.user).last()
            form.draft = last_draft
            # Finally, save the new instance.
            form.save()
            # And redirect to the monitoring page.
            return redirect(
                f"/monitoring?user={request.user.id}?destination={last_draft}"
            )

    # To display the empty wallet form.
    else:
        wallet_form = WalletCreationForm()

    # What to render to the template.
    last_draft = Draft.objects.filter(user=request.user).last()
    context = {"wallet_form": wallet_form, "last_draft": last_draft}

    return render(request, "wallet.html", context)


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def wallet_withdrawal(request):
    """
    View to the credit card withdrawal page.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    # When the form has been posted.
    if request.method == "POST":
        # Checking if the form has been validated.
        withdrawal_form = WalletWithdrawalForm(request.user, request.POST)
        if withdrawal_form.is_valid():
            # Saving the data from the withdrawal form to the database.
            withdrawal_form.save()
            # And redirect to the monitoring page.
            return redirect(
                f"/monitoring?user={request.user.id}?destination={last_draft}"
            )

    # To display the empty wallet withdrawal form.
    else:
        withdrawal_form = WalletWithdrawalForm(request.user)

    # What to render to the template.
    context = {"withdrawal_form": withdrawal_form, "last_draft": last_draft}

    return render(request, "withdrawal.html", context)


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def wallet_change(request):
    """
    View to the currency change page.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    # When the form has been posted.
    if request.method == "POST":
        # Checking if the form has been validated.
        change_form = WalletChangeForm(request.user, request.POST)
        if change_form.is_valid():
            # Saving the data from the change form to the database.
            change_form.save()
            # And redirect to the monitoring page.
            return redirect(
                f"/monitoring?user={request.user.id}?destination={last_draft}"
            )

    # To display the empty wallet change form.
    else:
        change_form = WalletChangeForm(request.user)

    # What to render to the template.
    context = {"change_form": change_form, "last_draft": last_draft}

    return render(request, "change.html", context)
