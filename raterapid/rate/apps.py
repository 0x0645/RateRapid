# coding=utf-8
"""Rate App Apps."""

from django.apps import AppConfig


class RateConfig(AppConfig):
    """Class representing the Rate app and its configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "raterapid.rate"
    verbose_name = "Rate"
