# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
monitoring URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [path("", views.monitoring, name="monitoring")]
