# -*- coding: utf-8 -*-
# pylint: disable=
"""All the views for the account app of the travel_budgeter project."""

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    """View to the user account creation page and validation of the user form."""
    # Analysis and treatment of the register form that has been sent.
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            # If data are valid, automatic log in and redirection to Draft page.
            login(request, user)
            return redirect("draft")
    else:
        form = UserCreationForm()

    # What to render to the template.
    context = {"form": form}
    return render(request, "register.html", context)
