# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""All the views for the monitoring app of the travel_budgeter project."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from draft.models import Draft
from expenses.models import Expense
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
        wallet_currency = wallet.currency
        # Balance calculation for each wallet considering expenses.
        expenses_sum = _expense_calculation(wallet, wallet_currency)
        # Balance calculation for each wallet considering withdrawals.
        withdrawal_sum = _withdrawal_calculation(wallet, wallet_currency)
        # Balance calculation for each wallet considering changes.
        change_sum = _change_calculation(wallet, wallet_currency)
        # Balance calculation for each wallet after all transactions.
        w_balance = initial_balance - expenses_sum - withdrawal_sum - change_sum
        wallet_dict[wallet.id] = w_balance

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
    withdrawal_amount_list = []
    for withdrawal in withdrawals_out_queryset:
        withdrawal_out_amount = withdrawal.amount
        withdrawal_in_currency = withdrawal.currency.iso
        if wallet_currency != withdrawal_in_currency:
            withdrawal_date = withdrawal.date
            currency_rate = CurrencyConverter(
                withdrawal_in_currency, wallet_currency, withdrawal_date
            ).exchange()
            withdrawal_out_amount *= currency_rate
        withdrawal_amount_list.append(withdrawal_out_amount)
    withdrawal_sum = sum(withdrawal_amount_list)
    return withdrawal_sum


def _change_calculation(wallet, wallet_currency):
    changes_out_queryset = Change.objects.filter(payment_type_out=wallet.id)
    change_amount_list = []
    for change in changes_out_queryset:
        change_out_amount = change.amount
        change_in_currency = change.currency_in.iso
        if wallet_currency != change_in_currency:
            change_date = change.date
            currency_rate = CurrencyConverter(
                change_in_currency, wallet_currency, change_date
            ).exchange()
            change_out_amount *= currency_rate
        change_amount_list.append(change_out_amount)
    change_sum = sum(change_amount_list)
    return change_sum
