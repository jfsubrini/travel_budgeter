# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
monitoring URL Configuration
"""
from django.urls import path
from . import views


urlpatterns = [
    path("", views.monitoring, name="monitoring"),
    path("wallet/balance/", views.wallet_balance, name="monitoring-wallet-balance"),
    path("wallet/category/", views.category_consumption, name="monitoring-category"),
    path(
        "wallet/category/simulation/",
        views.category_consumption_sim,
        name="monitoring-category-sim",
    ),
]
