# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
monitoring URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
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
    path(
        "wallet/category/today/",
        views.category_consumption_today,
        name="monitoring-category-today",
    ),
    path(
        "wallet/category/today/simulation/",
        views.category_consumption_today_sim,
        name="monitoring-category-today-sim",
    ),
    path(
        "wallet/category/7days/",
        views.category_consumption_7days,
        name="monitoring-category-7days",
    ),
    path(
        "wallet/category/7days/simulation/",
        views.category_consumption_7days_sim,
        name="monitoring-category-7days-sim",
    ),
    path("wallet/list-expenses/", views.list_expenses, name="monitoring-list-expenses"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
