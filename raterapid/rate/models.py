# coding=utf-8
"""Rate App Models."""

from django.db import models
from django.utils import timezone

from raterapid.core.models import TimeStampedModel


class Currency(models.TextChoices):
    """All Available Currencies."""

    USD = "USD"
    EGP = "EGP"
    EUR = "EUR"


class CurrencyConversion(TimeStampedModel):
    """Model to track the number of times specific currency conversion requests have been made."""

    from_currency = models.CharField(
        max_length=3, choices=Currency.choices, null=False, blank=False, verbose_name="Base Currency"
    )
    to_currency = models.CharField(
        max_length=3, choices=Currency.choices, null=False, blank=False, verbose_name="Target Currency"
    )
    count = models.IntegerField(default=1, verbose_name="Request Count")

    class Meta:
        """Meta Class."""

        unique_together = ("from_currency", "to_currency")
        ordering = ["-count"]
        verbose_name = "Currency Conversion"
        verbose_name_plural = "Currency Conversions"

    def increment_count(self) -> None:
        """Increments the count of currency conversion requests by one."""
        self.count += 1
        self.updated_at = timezone.now()
        self.save(update_fields=["count", "updated_at"])

    @classmethod
    def get_or_increment(cls, from_currency: str, to_currency: str) -> "CurrencyConversion":
        """Gets a CurrencyConversion instance, incrementing the count if it already exists."""
        currency_conversion, created = cls.objects.get_or_create(from_currency=from_currency, to_currency=to_currency)
        if not created:
            currency_conversion.increment_count()

        return currency_conversion
