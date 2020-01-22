# -*- coding: utf-8 -*-
# pylint: disable=no-member,too-many-locals,line-too-long
"""All the views for the monitoring app of the travel_budgeter project."""

from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from draft.models import Draft
from expenses.models import Expense, CATEGORY
from wallet.models import Withdrawal, Change
from .currency_api import CurrencyConverter


######################
#### GENERAL PAGE ####
######################
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def monitoring(request):
    """
    View to the monitoring page.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    context = {"user": request.user, "last_draft": last_draft}
    return render(request, "monitoring.html", context)


##############################
#### WALLETS BALANCE PAGE ####
##############################
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

    return change_out_sum, change_in_sum


################################################################
#### CATEGORY CONSUMPTION WITH SIMULATION PAGE - UP TO DATE ####
################################################################
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def category_consumption_sim(request):
    """
    View to the category consumption page, with simulation(s).
    """
    draft_categories_dict, expenses_cat_sim_dict, category_sim_ratio_dict, draft_global, expenses_global_sim, global_sim_ratio = _common_algo(
        request
    )

    context = {
        "draft_categories_dict": draft_categories_dict,
        "expenses_cat_sim_dict": expenses_cat_sim_dict,
        "category_sim_ratio_dict": category_sim_ratio_dict,
        "draft_global": draft_global,
        "expenses_global_sim": expenses_global_sim,
        "global_sim_ratio": global_sim_ratio,
    }

    return render(request, "current_category_sim.html", context)


###################################################################
#### CATEGORY CONSUMPTION WITHOUT SIMULATION PAGE - UP TO DATE ####
###################################################################
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def category_consumption(request):
    """
    View to the category consumption page, without simulation.
    """
    draft_categories_dict, expenses_categories_dict, category_ratio_dict, draft_global, expenses_global, global_ratio = _common_algo(
        request, False
    )

    context = {
        "draft_categories_dict": draft_categories_dict,
        "expenses_categories_dict": expenses_categories_dict,
        "category_ratio_dict": category_ratio_dict,
        "draft_global": draft_global,
        "expenses_global": expenses_global,
        "global_ratio": global_ratio,
    }

    return render(request, "current_category.html", context)


##############################################################################
#### CATEGORY CONSUMPTION WITH SIMULATION PAGE - JUST FOR ONE DAY (TODAY) ####
##############################################################################
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def category_consumption_today_sim(request):
    """
    View to the today's category consumption page, with simulation(s).
    """
    today = date.today()
    expenses_today_cat_sim_dict, category_today_sim_ratio_dict, draft_global_day, expenses_today_global_sim, global_day_sim_ratio = _common_algo_days(
        request, day=today
    )

    context = {
        "expenses_today_cat_sim_dict": expenses_today_cat_sim_dict,
        "category_today_sim_ratio_dict": category_today_sim_ratio_dict,
        "draft_global_day": draft_global_day,
        "expenses_today_global_sim": expenses_today_global_sim,
        "global_day_sim_ratio": global_day_sim_ratio,
    }

    return render(request, "today_category_sim.html", context)


#################################################################################
#### CATEGORY CONSUMPTION WITHOUT SIMULATION PAGE - JUST FOR ONE DAY (TODAY) ####
#################################################################################
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def category_consumption_today(request):
    """
    View to the today's category consumption page, without simulation.
    """
    today = date.today()
    expenses_today_cat_dict, category_today_ratio_dict, draft_global_day, expenses_today_global, global_day_ratio = _common_algo_days(
        request, False, day=today
    )

    context = {
        "expenses_today_cat_dict": expenses_today_cat_dict,
        "category_today_ratio_dict": category_today_ratio_dict,
        "draft_global_day": draft_global_day,
        "expenses_today_global": expenses_today_global,
        "global_day_ratio": global_day_ratio,
    }

    return render(request, "today_category.html", context)


#########################################################################
#### CATEGORY CONSUMPTION WITH SIMULATION PAGE - FOR THE LAST 7 DAYS ####
#########################################################################
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def category_consumption_7days_sim(request):
    """
    View to the last 7 days category consumption page, with simulation(s).
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    last_draft_currency = last_draft.currency
    last_draft_days = last_draft.travel_duration

    # Gathering all the draft categories amounts.
    draft_categories_dict = _draft_categories(last_draft)

    # Gathering all the last 7 days' expenses categories amounts, with the simulation(s).
    today = date.today()  # TODO
    expenses_queryset = Expense.objects.filter(draft=last_draft, date=today)  # TODO
    expenses_7days_cat_sim_dict = {}
    for expense in expenses_queryset:
        expense_category = expense.category
        expense_amount = expense.amount
        expense_currency = expense.currency.iso
        if last_draft_currency != expense_currency:
            expense_date = expense.date
            currency_rate = CurrencyConverter(
                expense_currency, last_draft_currency, expense_date
            ).exchange()
            expense_amount *= currency_rate
        if CATEGORY[expense_category - 1] not in expenses_7days_cat_sim_dict.keys():
            expenses_7days_cat_sim_dict[CATEGORY[expense_category - 1]] = expense_amount
        else:
            expenses_7days_cat_sim_dict[
                CATEGORY[expense_category - 1]
            ] += expense_amount

    # Ratio between expenses and draft for each category, with simulation(s).
    category_7days_sim_ratio_dict = {}
    for category, amount in expenses_7days_cat_sim_dict.items():
        if draft_categories_dict[category]:
            category_7days_sim_ratio_dict[category] = (
                amount / draft_categories_dict[category] * 100
            )
        else:
            category_7days_sim_ratio_dict[category] = None

    # Global consumption ratio, with simulation(s).
    del draft_categories_dict["Dépenses avant le départ"]
    del draft_categories_dict["Transport international"]
    draft_global_7days = sum(draft_categories_dict.values()) / last_draft_days  # TODO
    expenses_7days_global_sim = sum(expenses_7days_cat_sim_dict.values())
    global_7days_sim_ratio = expenses_7days_cat_sim_dict / draft_global_7days * 100

    context = {
        "expenses_7days_cat_sim_dict": expenses_7days_cat_sim_dict,
        "category_7days_sim_ratio_dict": category_7days_sim_ratio_dict,
        "draft_global_7days": draft_global_7days,
        "expenses_7days_global_sim": expenses_7days_global_sim,
        "global_7days_sim_ratio": global_7days_sim_ratio,
    }

    return render(request, "7days_category_sim.html", context)


############################################################################
#### CATEGORY CONSUMPTION WITHOUT SIMULATION PAGE - FOR THE LAST 7 DAYS ####
############################################################################
@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def category_consumption_7days(request):
    """
    View to the today's category consumption page, without simulation.
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    last_draft_currency = last_draft.currency
    last_draft_days = last_draft.travel_duration

    # Gathering all the draft categories amounts.
    draft_categories_dict = _draft_categories(last_draft)

    # Gathering all the last 7 days' expenses categories amounts, with the simulation(s).
    today = date.today()  # TODO
    expenses_queryset = Expense.objects.filter(
        draft=last_draft, date=today, simulation=False
    )  # TODO
    expenses_7days_cat_dict = {}
    for expense in expenses_queryset:
        expense_category = expense.category
        expense_amount = expense.amount
        expense_currency = expense.currency.iso
        if last_draft_currency != expense_currency:
            expense_date = expense.date
            currency_rate = CurrencyConverter(
                expense_currency, last_draft_currency, expense_date
            ).exchange()
            expense_amount *= currency_rate
        if CATEGORY[expense_category - 1] not in expenses_7days_cat_dict.keys():
            expenses_7days_cat_dict[CATEGORY[expense_category - 1]] = expense_amount
        else:
            expenses_7days_cat_dict[CATEGORY[expense_category - 1]] += expense_amount

    # Ratio between expenses and draft for each category, with simulation(s).
    category_7ays_ratio_dict = {}
    for category, amount in expenses_7days_cat_dict.items():
        if draft_categories_dict[category]:
            category_7ays_ratio_dict[category] = (
                amount / draft_categories_dict[category] * 100
            )
        else:
            category_7ays_ratio_dict[category] = None

    # Global consumption ratio, with simulation(s).
    del draft_categories_dict["Dépenses avant le départ"]
    del draft_categories_dict["Transport international"]
    draft_global_7days = sum(draft_categories_dict.values()) / last_draft_days  # TODO
    expenses_7days_global = sum(expenses_7days_cat_dict.values())
    global_7days_ratio = expenses_7days_global / draft_global_7days * 100

    context = {
        "expenses_7days_cat_dict": expenses_7days_cat_dict,
        "category_7ays_ratio_dict": category_7ays_ratio_dict,
        "draft_global_7days": draft_global_7days,
        "expenses_7days_global": expenses_7days_global,
        "global_7days_ratio": global_7days_ratio,
    }

    return render(request, "7days_category.html", context)


def _common_algo(request, *simulation):
    """
    Common algo for category consumption functions, with or without simulation(s).
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    last_draft_currency = last_draft.currency

    # Gathering all the draft categories amounts.
    draft_categories_dict = _draft_categories(last_draft)

    # Gathering all the expenses categories amounts, with or without simulation(s).
    if simulation:
        expenses_queryset = Expense.objects.filter(
            draft=last_draft, simulation=simulation[0]
        )
    else:
        expenses_queryset = Expense.objects.filter(draft=last_draft)

    expenses_categories_dict = {}
    for expense in expenses_queryset:
        expense_category = expense.category
        expense_amount = expense.amount
        expense_currency = expense.currency.iso
        if last_draft_currency != expense_currency:
            expense_date = expense.date
            currency_rate = CurrencyConverter(
                expense_currency, last_draft_currency, expense_date
            ).exchange()
            expense_amount *= currency_rate
        if CATEGORY[expense_category - 1] not in expenses_categories_dict.keys():
            expenses_categories_dict[CATEGORY[expense_category - 1]] = expense_amount
        else:
            expenses_categories_dict[CATEGORY[expense_category - 1]] += expense_amount

    # Ratio between expenses and draft for each category, with or without simulation(s).
    category_ratio_dict = {}
    for category, amount in expenses_categories_dict.items():
        if draft_categories_dict[category]:
            category_ratio_dict[category] = (
                amount / draft_categories_dict[category] * 100
            )
        else:
            category_ratio_dict[category] = None

    # Global consumption ratio, with or without simulation(s).
    draft_global = sum(draft_categories_dict.values())
    expenses_global = sum(expenses_categories_dict.values())
    global_ratio = expenses_global / draft_global * 100

    return (
        draft_categories_dict,
        expenses_categories_dict,
        category_ratio_dict,
        draft_global,
        expenses_global,
        global_ratio,
    )


def _common_algo_days(request, *simulation, day):
    """
    Common algo for today's or for 7 days category consumption functions, with or without simulation(s).
    """
    last_draft = Draft.objects.filter(user=request.user).last()
    last_draft_currency = last_draft.currency
    last_draft_days = last_draft.travel_duration

    # Gathering all the draft categories amounts.
    draft_categories_dict = _draft_categories(last_draft)

    # Gathering all the today's expenses categories amounts, with or without simulation(s).
    if simulation:
        expenses_queryset = Expense.objects.filter(
            draft=last_draft, date=day, simulation=simulation[0]
        )
    else:
        expenses_queryset = Expense.objects.filter(draft=last_draft, date=day)

    expenses_day_cat_dict = {}
    for expense in expenses_queryset:
        expense_category = expense.category
        expense_amount = expense.amount
        expense_currency = expense.currency.iso
        if last_draft_currency != expense_currency:
            expense_date = expense.date
            currency_rate = CurrencyConverter(
                expense_currency, last_draft_currency, expense_date
            ).exchange()
            expense_amount *= currency_rate
        if CATEGORY[expense_category - 1] not in expenses_day_cat_dict.keys():
            expenses_day_cat_dict[CATEGORY[expense_category - 1]] = expense_amount
        else:
            expenses_day_cat_dict[CATEGORY[expense_category - 1]] += expense_amount

    # Ratio between expenses and draft for each category, with or without simulation(s).
    category_day_ratio_dict = {}
    for category, amount in expenses_day_cat_dict.items():
        if draft_categories_dict[category]:
            category_day_ratio_dict[category] = (
                amount / draft_categories_dict[category] * 100
            )
        else:
            category_day_ratio_dict[category] = None

    # Global consumption ratio, with or without simulation(s).
    del draft_categories_dict["Dépenses avant le départ"]
    del draft_categories_dict["Transport international"]
    draft_global_day = sum(draft_categories_dict.values()) / last_draft_days
    expenses_day_global = sum(expenses_day_cat_dict.values())
    global_day_ratio = expenses_day_global / draft_global_day * 100

    return (
        expenses_day_cat_dict,
        category_day_ratio_dict,
        draft_global_day,
        expenses_day_global,
        global_day_ratio,
    )


def _draft_categories(last_draft):
    """
    Gathering all the draft categories amounts.
    """
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
        CATEGORY[0]: draft_pre_departure or 0,
        CATEGORY[1]: draft_international_transport or 0,
        CATEGORY[2]: draft_local_transport or 0,
        CATEGORY[3]: draft_lodging or 0,
        CATEGORY[4]: draft_fooding or 0,
        CATEGORY[5]: draft_visiting or 0,
        CATEGORY[6]: draft_activities or 0,
        CATEGORY[7]: draft_souvenirs or 0,
        CATEGORY[8]: draft_various or 0,
    }
    return draft_categories_dict
