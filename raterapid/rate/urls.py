# coding=utf-8
"""Rate App URLS."""
from django.urls import path

from .views import CurrencyConversionView

urlpatterns = [
    path("conversion/", CurrencyConversionView.as_view(), name="conversion"),
]
