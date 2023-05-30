"""Factories for creating fake users for testing."""
from django.contrib.auth.models import User
from factory import Faker
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """Create fake users for testing."""

    class Meta:
        """Meta class for UserFactory."""

        model = User

    username = Faker("user_name")
    password = Faker("password")
    email = Faker("email")


__all__ = ["UserFactory"]
