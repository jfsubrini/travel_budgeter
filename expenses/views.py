# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""All the views for the expenses app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from draft.models import Draft
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
        expense_form = ExpenseForm(request.user, request.POST)
        if expense_form.is_valid():
            # Saving the data from the expense form to the database.
            # First, create, but don't save the new Expense instance.
            form = expense_form.save(commit=False)
            # Then, link the instance with the last draft from that logged travel user.
            last_draft = Draft.objects.filter(user=request.user).last()
            form.draft = last_draft
            # Finally, save the new instance.
            form.save()
            # And redirect to the monitoring page.
            return redirect(
                f"/monitoring?user={request.user.id}?destination={last_draft}"
            )

    # To display the empty expense form.
    else:
        expense_form = ExpenseForm(request.user)

    # What to render to the template.
    last_draft = Draft.objects.filter(user=request.user).last()
    context = {"expense_form": expense_form, "last_draft": last_draft}

    return render(request, "expenses.html", context)
