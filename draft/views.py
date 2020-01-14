# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the draft app of the travel_budgeter project."""

from django.shortcuts import render, redirect

from .forms import DraftForm, DraftForm2
from .models import Category, Draft


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
            # # Create and save the new TravelUser instance.
            # tu_form.save()
            # Saving the data from the forms to the database and redirect to the outliers page.
            user = _save_forms(draft_form, draft2_form)
            return redirect(f"/reco/outliers?submitted=True&user={user.id}")

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


def _save_forms(draft_form, draft2_form, user_email):
    """Saving the data from the forms to the database and redirect to the outliers page."""
    # Create, but don't save the new LikeDislikeSurvey
    # and TravellingConditionsSurvey instances.
    form1 = draft_form.save(commit=False)
    form6 = tc_form.save(commit=False)
    # Link the instance with a specific travel user (the one that made the interview).
    # Save the new instance.
    user = TravelUser.objects.get(email=user_email)
    form1.travel_user = user
    form1.save()
    # Idem with the last LikeDislike survey linked with that travel user.
    # Save new instances and then the many-to-many data for the form (when existing).
    survey = LikeDislikeSurvey.objects.filter(travel_user__email=user_email).last()
    # animals
    animal_list = ld2_form.cleaned_data["animal_name"]
    for animal in animal_list:
        form2 = Animal.objects.get(animal_name=animal)
        survey.animals.add(form2.id)
    # landscapes
    landscape_list = ld3_form.cleaned_data["landscape_name"]
    for landscape in landscape_list:
        form3 = Landscape.objects.get(landscape_name=landscape)
        survey.landscapes.add(form3.id)
    # outdoor activities
    outdoor_list = ld4_form.cleaned_data["outdoor_activity_name"]
    for outdoor in outdoor_list:
        form4 = OutdoorActivity.objects.get(outdoor_activity_name=outdoor)
        survey.outdoor_acivities.add(form4.id)
    # urban activities
    urban_list = ld5_form.cleaned_data["urban_activity_name"]
    for urban in urban_list:
        form5 = UrbanActivity.objects.get(urban_activity_name=urban)
        survey.urban_activities.add(form5.id)
    # travelling conditions
    form6.survey_like = survey
    form6.travel_user = user
    form6.save()
    # Idem with the last TravellingConditions survey linked with that travel user.
    condition_survey = TravellingConditionsSurvey.objects.filter(
        travel_user__email=user_email
    ).last()
    language_list = tc2_form.cleaned_data["language_name"]
    for language in language_list:
        form7 = LanguageSpoken.objects.get(language_name=language)
        condition_survey.languages_spoken.add(form7.id)
    return user
