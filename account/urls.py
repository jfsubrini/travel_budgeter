# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
account URL Configuration
"""
from django.contrib.auth.views import LoginView
from django.urls import path

from . import views


urlpatterns = [
    path("register", views.register, name="register"),
    path("signin", LoginView.as_view(template_name="signin.html"), name="signin"),
]
