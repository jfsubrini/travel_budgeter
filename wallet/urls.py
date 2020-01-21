# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
wallet URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [
    path("creation/", views.wallet_creation, name="wallet-creation"),
    path("withdrawal/", views.wallet_withdrawal, name="wallet-withdrawal"),
    path("change/", views.wallet_change, name="wallet-change"),
]
