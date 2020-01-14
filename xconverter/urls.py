# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
xconverter URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [path("", views.converter, name="converter")]
