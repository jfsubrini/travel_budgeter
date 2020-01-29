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


#########################################@
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def select_wallet(request):
    #     """
    #     View to a page where the travel user can select a draft to be edited.
    #     """
    #     # When the form has been posted.
    #     if request.method == "POST":
    #         # Checking if the form has been validated.
    #         select_draft_form = SelectDraftForm(request.user, request.POST)
    #         if select_draft_form.is_valid():
    #             # Catching the form radio choice.
    #             select_draft_id = select_draft_form.cleaned_data["select_draft"].id
    #             # And redirect to the monitoring page.
    #             return redirect(
    #                 f"/draft/edit?user={request.user.id}&destination={select_draft_id}"
    #             )

    #     # To display the empty select draft form.
    #     else:
    #         select_draft_form = SelectDraftForm(user=request.user)

    # What to render to the template.
    context = {"select_wallet_form": select_wallet_form}

    return render(request, "select_wallet.html", context)


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def edit_wallet(request):
    # """
    # View to an existing travel user draft to be modified.
    # """
    #     # Get the right draft and catch the value of its different fields.
    #     select_draft_id = request.GET["destination"]
    #     selected_draft = Draft.objects.get(id=select_draft_id)
    #     selected_draft_category = Category.objects.get(draft=select_draft_id)

    #     # Analysis and treatment of the draft form that has been sent.
    #     # When the forms has been posted.
    #     if request.method == "POST":
    #         # Checking if the forms have been validated.
    #         edit_draft_form = EditDraftForm(selected_draft, request.POST)
    #         edit_draft2_form = EditDraftForm2(selected_draft_category, request.POST)
    #         if edit_draft_form.is_valid() and edit_draft2_form.is_valid():
    #             # Saving the data from the draft forms to update the data from the database.
    #             form1 = edit_draft_form.save(commit=False)
    #             form2 = edit_draft2_form.save(commit=False)
    #             # Updating the category data for the id related to the draft to be modified.
    #             form2.id = selected_draft_category.id
    #             form2.save()
    #             # Updating the other draft data for the one to be modified.
    #             form1.id = selected_draft.id
    #             form1.user = request.user
    #             form1.category = selected_draft_category
    #             form1.save()
    #             # Redirecting to the wallet creation page.
    #             return redirect(
    #                 f"/monitoring?user={request.user.id}&destination={selected_draft}"
    #             )

    #     # To display the draft forms with all the instance data in the placeholders.
    #     # The first one about travel data and the second one about the draft budget for each category.
    #     else:
    #         edit_draft_form = EditDraftForm(instance=selected_draft)
    #         edit_draft2_form = EditDraftForm2(instance=selected_draft_category)

    # What to render to the template.
    context = {"edit_wallet_form": edit_wallet_form, "selected_wallet": selected_wallet}

    return render(request, "edit_wallet.html", context)
