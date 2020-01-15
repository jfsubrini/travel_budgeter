# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
expenses URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [path("", views.expenses, name="expenses")]
