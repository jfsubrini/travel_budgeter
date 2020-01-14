# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
wallet URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [path("", views.wallet, name="wallet")]
