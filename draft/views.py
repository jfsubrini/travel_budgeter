# -*- coding: utf-8 -*-
# pylint: disable=no-member
"""All the views for the draft app of the travel_budgeter project."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import DraftForm, DraftForm2, SelectDraftForm
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
def select_draft(request):
    """
    View to a page where the travel user can select a draft to be edited.
    """
    # When the form has been posted.
    if request.method == "POST":
        # Checking if the form has been validated.
        select_draft_form = SelectDraftForm(request.user, request.POST)
        if select_draft_form.is_valid():
            # Catching the form radio choice.
            select_draft_id = select_draft_form.cleaned_data["select_draft"].id
            # And redirect to the monitoring page.
            return redirect(
                f"/draft/edit?user={request.user.id}&destination={select_draft_id}"
            )

    # To display the empty select draft form.
    else:
        select_draft_form = SelectDraftForm(user=request.user)

    # What to render to the template.
    context = {"select_draft_form": select_draft_form}

    return render(request, "select_draft.html", context)


@login_required(login_url="/signin/", redirect_field_name="redirection_vers")
def edit_draft(request):
    """
    View to an existing travel user draft to be modified.
    """
    # Get the right draft and catch the value of its different fields.
    select_draft_id = request.GET["destination"]
    selected_draft = Draft.objects.get(id=select_draft_id)
    departure_date = selected_draft.departure_date
    travel_duration = selected_draft.travel_duration
    pre_departure = selected_draft.category.pre_departure
    international_transport = selected_draft.category.international_transport
    local_transport = selected_draft.category.local_transport
    lodging = selected_draft.category.lodging
    fooding = selected_draft.category.fooding
    visiting = selected_draft.category.visiting
    activities = selected_draft.category.activities
    souvenirs = selected_draft.category.souvenirs
    various = selected_draft.category.various

    # # Analysis and treatment of the draft form that has been sent.
    # submitted = False
    # # When the forms has been posted.
    # if request.method == "POST":
    #     # # Checking if the forms have been validated.
    #     # draft_form = DraftForm(request.POST)
    #     # draft2_form = DraftForm2(request.POST)
    #     # if draft_form.is_valid() and draft2_form.is_valid():
    #     #     # Saving the data from the draft forms to the database.
    #     #     form1 = draft_form.save(commit=False)
    #     #     form2 = draft2_form.save(commit=False)
    #     #     # Link the instance with a specific travel user (the one that made the draft).
    #     #     travel_user = User.objects.get(
    #     #         username=request.user.username, password=request.user.password
    #     #     )
    #     #     form1.user = travel_user
    #     #     form2.user = travel_user
    #     #     # Saving the categories data.
    #     #     form2.save()
    #     #     # Link the travel data with the right categories data (the last saved).
    #     #     draft_category = Category.objects.last()
    #     #     form1.category = draft_category
    #     #     form1.save()
    #     #     # Redirecting to the wallet creation page.
    #     return redirect(f"/wallet/creation?submitted=True&user={request.user.id}")

    # # To display the empty draft forms : the first one about travel data and
    # # the second one about the draft budget for each category.
    # else:
    #     edit_draft_form = EditDraftForm()
    #     if "submitted" in request.GET:
    #         submitted = True

    # What to render to the template.
    context = {
        # "edit_draft_form": edit_draft_form,
        "departure_date": departure_date,
        "travel_duration": travel_duration,
        "pre_departure": pre_departure,
        "international_transport": international_transport,
        "local_transport": local_transport,
        "lodging": lodging,
        "fooding": fooding,
        "visiting": visiting,
        "activities": activities,
        "souvenirs": souvenirs,
        "various": various,
    }

    return render(request, "edit_draft.html", context)
