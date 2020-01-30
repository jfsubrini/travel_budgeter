# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
draft URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [
    path("", views.draft, name="draft"),
    path("select/", views.select_draft, name="select-draft"),
    path("edit/", views.edit_draft, name="edit-draft"),
]
