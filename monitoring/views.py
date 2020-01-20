# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""All the views for the monitoring app of the travel_budgeter project."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from draft.models import Draft
from expenses.models import Expense
from .currency_api import CurrencyConverter


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def monitoring(request):
    """
    View to the monitoring balance page.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    wallet_queryset = last_draft.wallets.all()
    wallet_dict = {}
    for wallet in wallet_queryset:
        initial_balance = wallet.balance
        wallet_currency = wallet.currency
        expenses_related_queryset = Expense.objects.filter(
            payment_type=wallet, draft=last_draft
        )
        expense_amount_list = []
        for expense in expenses_related_queryset:
            # TODO pour crédit et pas que dépenses
            expense_amount = expense.amount
            expense_currency = expense.currency.iso
            if wallet_currency != expense_currency:
                expense_date = expense.date
                currency_rate = CurrencyConverter(
                    wallet_currency, expense_currency, expense_date
                ).exchange()  # TODO Attention pb car les dates sont dans le futur. Refaire les expenses avec dates dans le passé.
                expense_amount *= currency_rate
            expense_amount_list.append(expense_amount)
        wallet_balance = initial_balance - sum(expense_amount_list)
        wallet_dict[wallet.id] = wallet_balance

    context = {"wallet_dict": wallet_dict}
    return render(request, "balance.html", context)

