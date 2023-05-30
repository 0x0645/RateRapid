# coding=utf-8
"""User App Serializers."""

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Fields:
        username: The user's username.
        first_name: The user's first name.
        last_name: The user's last name.
        email: The user's email address.
        password: The user's password (write-only).
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        """Meta class for UserSerializer."""

        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        """Create a new User instance."""
        return User.objects.create_user(**validated_data)
