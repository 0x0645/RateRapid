# coding=utf-8
"""Rate App Serializers."""

from django.utils import timezone
from rest_framework import serializers

from .models import Currency


class CurrencyConversionSerializer(serializers.Serializer):
    """Serializer for currency conversion."""

    from_currency = serializers.ChoiceField(choices=Currency.choices)
    to_currency = serializers.ChoiceField(choices=Currency.choices)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class CurrencyConversionResponseSerializer(serializers.Serializer):
    """Serializer for currency conversion response."""

    time_now = serializers.DateTimeField(default=timezone.now)
    last_updated = serializers.DateTimeField()
    amount = serializers.FloatField()
    base = serializers.CharField(max_length=3)
    target = serializers.CharField(max_length=3)
