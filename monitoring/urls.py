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
        "wallet/category/today/",
        views.category_consumption_today,
        name="monitoring-category-today",
    ),
    path(
        "wallet/category/7days/",
        views.category_consumption_7days,
        name="monitoring-category-7days",
    ),
    path("wallet/list-expenses/", views.list_expenses, name="monitoring-list-expenses"),
    path(
        "wallet/delete-simulations/",
        views.delete_simulations,
        name="monitoring-delete-simulations",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
