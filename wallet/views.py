# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""All the views for the wallet app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from draft.models import Draft
from .forms import (
    WalletCreationForm,
    WalletWithdrawalForm,
    WalletChangeForm,
    SelectWalletForm,
    EditWalletForm,
)
from .models import PaymentType


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
        withdrawal_form = WalletWithdrawalForm(last_draft, request.POST)
        if withdrawal_form.is_valid():
            # Saving the data from the withdrawal form to the database.
            withdrawal_form.save()
            # And redirect to the monitoring page.
            return redirect(
                f"/monitoring?user={request.user.id}?destination={last_draft}"
            )

    # To display the empty wallet withdrawal form.
    else:
        withdrawal_form = WalletWithdrawalForm(last_draft)

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
        change_form = WalletChangeForm(last_draft, request.POST)
        if change_form.is_valid():
            # Saving the data from the change form to the database.
            change_form.save()
            # And redirect to the monitoring page.
            return redirect(
                f"/monitoring?user={request.user.id}?destination={last_draft}"
            )

    # To display the empty wallet change form.
    else:
        change_form = WalletChangeForm(last_draft)

    # What to render to the template.
    context = {"change_form": change_form, "last_draft": last_draft}

    return render(request, "change.html", context)


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def select_wallet(request):
    """
    View to a page where the travel user can select a wallet to be edited.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    # When the form has been posted.
    if request.method == "POST":
        # Checking if the form has been validated.
        select_wallet_form = SelectWalletForm(last_draft, request.POST)
        if select_wallet_form.is_valid():
            # Catching the form select choice.
            select_wallet_id = select_wallet_form.cleaned_data["select_wallet"].id
            # And redirect to the wallet/edit page.
            return redirect(
                f"/wallet/edit?user={request.user.id}&wallet={select_wallet_id}"
            )

    # To display the empty select draft form.
    else:
        select_wallet_form = SelectWalletForm(draft=last_draft)

    # What to render to the template.
    context = {"select_wallet_form": select_wallet_form, "last_draft": last_draft}

    return render(request, "select_wallet.html", context)


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def edit_wallet(request):
    """
    View to an existing travel user wallet to be modified.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    # Get the right wallet and catch the value of its different fields.
    select_wallet_id = request.GET["wallet"]
    selected_wallet = PaymentType.objects.get(id=select_wallet_id)

    # Analysis and treatment of the wallet form that has been sent.
    # When the form has been posted.
    if request.method == "POST":
        # Checking if the form has been validated.
        edit_draft_form = EditWalletForm(selected_wallet, request.POST)
        if edit_draft_form.is_valid():
            # Saving the data from the wallet form to update the data from the database.
            form = edit_draft_form.save(commit=False)
            # Updating the wallet data for the id related to the wallet to be modified.
            form.id = selected_wallet.id
            form.draft = selected_wallet.draft
            form.created_at = selected_wallet.created_at
            form.save()
            # Redirecting to the monitoring page.
            return redirect(
                f"/monitoring?user={request.user.id}&destination={last_draft}"
            )

    # To display the wallet form with all the instance data as default data.
    else:
        edit_wallet_form = EditWalletForm(instance=selected_wallet)

    # What to render to the template.
    context = {"edit_wallet_form": edit_wallet_form, "selected_wallet": selected_wallet}

    return render(request, "edit_wallet.html", context)
