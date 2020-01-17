# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the expenses app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ExpenseForm


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def expenses(request):
    """
    View to the expense page.
    """
    # Analysis and treatment of the expense form that has been sent.
    # When the form has been posted.
    if request.method == "POST":
        # Checking if the form has been validated.
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            # Saving the data from the expense form to the database.
            expense_form.save()
            # Redirecting to the monitoring page.
            return redirect(f"/monitoring?user={request.user.id}")

    # To display the empty expense form.
    else:
        expense_form = ExpenseForm()

    # What to render to the template.
    context = {"expense_form": expense_form}

    return render(request, "expenses.html", context)
