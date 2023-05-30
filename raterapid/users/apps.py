"""User App Apps."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Class representing the user application and its configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "raterapid.users"
    verbose_name = "User"
