# -*- coding: utf-8 -*-
# pylint: disable=no-member,too-many-locals
"""All the views for the monitoring app of the travel_budgeter project."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from draft.models import Draft
from expenses.models import Expense, CATEGORY
from wallet.models import Withdrawal, Change
from .currency_api import CurrencyConverter


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def monitoring(request):
    """
    View to the monitoring page.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    context = {"user": request.user, "last_draft": last_draft}
    return render(request, "monitoring.html", context)


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def wallet_balance(request):
    """
    View to the wallet balance page.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    wallet_queryset = last_draft.wallets.all()
    wallet_dict = {}
    # Balance calculation for each wallet (for the current draft).
    # TODO vérifier que les devises des comptes et porte-monnaies sont ok.
    for wallet in wallet_queryset:
        initial_balance = wallet.balance
        wallet_currency = wallet.currency.iso
        # Balance calculation for each wallet considering expenses.
        expenses_sum = _expense_calculation(wallet, wallet_currency)
        # Balance calculation for each wallet considering withdrawals.
        withdrawal_out_sum, withdrawal_in_sum = _withdrawal_calculation(
            wallet, wallet_currency
        )
        # Balance calculation for each wallet considering changes.
        change_out_sum, change_in_sum = _change_calculation(wallet, wallet_currency)
        # Balance calculation for each wallet after all transactions.
        w_balance = (
            initial_balance
            - expenses_sum
            - withdrawal_out_sum
            + withdrawal_in_sum
            - change_out_sum
            + change_in_sum
        )
        wallet_dict[wallet] = w_balance

    context = {"wallet_dict": wallet_dict}

    return render(request, "balance.html", context)


def _expense_calculation(wallet, wallet_currency):
    expenses_related_queryset = Expense.objects.filter(payment_type=wallet)
    expense_amount_list = []
    for expense in expenses_related_queryset:
        expense_amount = expense.amount
        expense_currency = expense.currency.iso
        if wallet_currency != expense_currency:
            expense_date = expense.date
            currency_rate = CurrencyConverter(
                expense_currency, wallet_currency, expense_date
            ).exchange()
            expense_amount *= currency_rate
        expense_amount_list.append(expense_amount)
    expenses_sum = sum(expense_amount_list)

    return expenses_sum


def _withdrawal_calculation(wallet, wallet_currency):
    withdrawals_out_queryset = Withdrawal.objects.filter(payment_type_out=wallet.id)
    withdrawals_in_queryset = Withdrawal.objects.filter(payment_type_in=wallet.id)
    # Calculate the sum to debit from the credit cards.
    withdrawal_out_amount_list = []
    for withdrawal in withdrawals_out_queryset:
        withdrawal_out_amount = withdrawal.amount
        withdrawal_in_currency = withdrawal.currency.iso
        if wallet_currency != withdrawal_in_currency:
            # When the rate is given by the user.
            if withdrawal.rate:
                currency_rate = withdrawal.rate
            # Else, online rate.
            else:
                withdrawal_date = withdrawal.date
                currency_rate = CurrencyConverter(
                    withdrawal_in_currency, wallet_currency, withdrawal_date
                ).exchange()
            withdrawal_out_amount *= currency_rate
        withdrawal_out_amount_list.append(withdrawal_out_amount)
    withdrawal_out_sum = sum(withdrawal_out_amount_list)
    # Calculate the sum to credit the wallets.
    withdrawal_in_amount_list = []
    for withdrawal in withdrawals_in_queryset:
        withdrawal_in_amount = withdrawal.amount
        withdrawal_in_amount_list.append(withdrawal_in_amount)
    withdrawal_in_sum = sum(withdrawal_in_amount_list)

    return withdrawal_out_sum, withdrawal_in_sum


def _change_calculation(wallet, wallet_currency):  # TODO A REVOIR TOUT ICI
    changes_out_queryset = Change.objects.filter(payment_type_out=wallet.id)
    changes_in_queryset = Change.objects.filter(payment_type_in=wallet.id)
    # Calculate the sum to debit from the wallet of the currency to change.
    change_out_amount_list = []
    for change in changes_out_queryset:
        change_out_amount = change.amount
        change_in_currency = change.currency_in.iso
        if wallet_currency != change_in_currency:
            change_date = change.date
            currency_rate = CurrencyConverter(
                change_in_currency, wallet_currency, change_date
            ).exchange()
            change_out_amount *= currency_rate
        change_out_amount_list.append(change_out_amount)
    change_out_sum = sum(change_out_amount_list)
    # Calculate the sum to credit the wallets.
    change_in_amount_list = []
    for change in changes_in_queryset:
        change_in_amount = change.amount
        change_in_amount_list.append(change_in_amount)
    change_in_sum = sum(change_in_amount_list)
    print("change_in_sum ... :", change_in_sum)

    return change_out_sum, change_in_sum


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def category_consumption(request):
    """
    View to the category consumption page.
    """
    # Gathering all the draft categories amounts.
    last_draft = Draft.objects.filter(user=request.user).last()
    draft_categories = last_draft.category
    draft_pre_departure = draft_categories.pre_departure
    draft_international_transport = draft_categories.international_transport
    draft_local_transport = draft_categories.local_transport
    draft_lodging = draft_categories.lodging
    draft_fooding = draft_categories.fooding
    draft_visiting = draft_categories.visiting
    draft_activities = draft_categories.activities
    draft_souvenirs = draft_categories.souvenirs
    draft_various = draft_categories.various
    draft_categories_dict = {
        CATEGORY[0]: draft_pre_departure,
        CATEGORY[1]: draft_international_transport,
        CATEGORY[2]: draft_local_transport,
        CATEGORY[3]: draft_lodging,
        CATEGORY[4]: draft_fooding,
        CATEGORY[5]: draft_visiting,
        CATEGORY[6]: draft_activities,
        CATEGORY[7]: draft_souvenirs,
        CATEGORY[8]: draft_various,
    }
    # Gathering all the expenses categories amounts.
    expenses_queryset = Expense.objects.filter(draft=last_draft)
    expenses_categories_dict = {}
    i = 0
    for expense in expenses_queryset:
        expense_category = expense.category
        expenses_categories_dict[CATEGORY[i]] = expense_category
        i += 1
    # Ratio between expenses and draft for each category.
    category_ratio_dict = {}
    for category, amount in expenses_categories_dict.items():
        category_ratio_dict[category] = amount / draft_categories_dict[category] * 100

    context = {
        "draft_categories_dict": draft_categories_dict,
        "expenses_categories_dict": expenses_categories_dict,
        "category_ratio_dict": category_ratio_dict,
    }

    return render(request, "category.html", context)
