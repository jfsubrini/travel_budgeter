# -*- coding: utf-8 -*-
# pylint: disable=no-member
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
    # Analysis and treatment of the draft form that has been sent.
    submitted = False
    # When the forms has been posted.
    if request.method == "POST":
        # Checking if the forms have been validated.
        draft_form = DraftForm(request.POST)
        draft2_form = DraftForm2(request.POST)
        if draft_form.is_valid() and draft2_form.is_valid():
            # Saving the data from the draft forms to the database.
            form1 = draft_form.save(commit=False)
            form2 = draft2_form.save(commit=False)
            # Link the instance with a specific travel user (the one that made the draft).
            travel_user = User.objects.get(
                username=request.user.username, password=request.user.password
            )
            form1.user = travel_user
            form2.user = travel_user
            # Saving the categories data.
            form2.save()
            # Link the travel data with the right categories data (the last saved).
            draft_category = Category.objects.last()
            form1.category = draft_category
            form1.save()
            # Redirecting to the wallet creation page.
            return redirect(f"/wallet/creation?submitted=True&user={request.user.id}")

    # To display the empty draft forms : the first one about travel data and
    # the second one about the draft budget for each category.
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


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def edit_draft(request):
    """
    View to an existing travel user draft to be modified.
    """
    travel_user = User.objects.get(
        username=request.user.username, password=request.user.password
    )
    user_drafts = Draft.objects.filter(user=travel_user)

    # What to render to the template.
    context = {"user_drafts": user_drafts}

    return render(request, "edit_draft.html", context)
