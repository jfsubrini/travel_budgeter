# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
wallet URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [path("creation/", views.wallet_creation, name="wallet_creation")]
