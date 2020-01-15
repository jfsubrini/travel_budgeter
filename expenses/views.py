# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the expenses app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import ExpenseForm


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def expenses(request):
    """
    View to the expenses page.
    """
    # Analysis and treatment of the expense form that has been sent.
    # When the form has been posted.
    if request.method == "POST":
        print("ICI 2")
        # Checking if the form has been validated.
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            # Saving the data from the expense form to the database.
            form = expense_form.save(commit=False)
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

    # To display the empty expense form.
    else:
        expense_form = ExpenseForm()

    # What to render to the template.
    context = {"expense_form": expense_form}

    return render(request, "expenses.html", context)
