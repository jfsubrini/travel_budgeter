# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the draft app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import DraftForm, DraftForm2
from .models import Category, Draft


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def draft(request):
    """
    View to the travel user draft form page.
    """
    # Analysis and treatment of the register form that has been sent.
    submitted = False
    # When the interview has been posted
    if request.method == "POST":
        # Checking if the forms has been validated.
        draft_form = DraftForm(request.POST)
        draft2_form = DraftForm2(request.POST)
        if draft_form.is_valid() and draft2_form.is_valid():
            # Saving the data from the forms to the database and redirect to the expenses page.
            travel_user = User.objects.get(username=username, password=password)
            user = _save_forms(
                draft_form, draft2_form, travel_user.username, travel_user.password
            )
            return redirect(f"/expenses/new_expense?submitted=True&user={user.id}")

    # To display the empty interview forms.
    else:
        draft_form = DraftForm()
        draft2_form = DraftForm2()
        if "submitted" in request.GET:
            submitted = True

    # What to render to the template.
    context = {
        "draft_form": draft_form,
        "draft2_form": draft2_form,
        "submitted": submitted,
    }

    return render(request, "draft.html", context)


def _save_forms(draft_form, draft2_form, username, password):
    """Saving the data from the forms to the database."""
    # Create, but don't save the new LikeDislikeSurvey
    # and TravellingConditionsSurvey instances.
    form1 = draft_form.save(commit=False)
    form2 = draft2_form.save(commit=False)
    # Link the instance with a specific travel user (the one that made the interview).
    # Save the new instance.
    travel_user = User.objects.get(username=username, password=password)
    form1.user = travel_user
    form1.save()

    return user
