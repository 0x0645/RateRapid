"""Rate App Admin."""

from django.contrib import admin

from .models import CurrencyConversion


@admin.register(CurrencyConversion)
class CurrencyConversionAdmin(admin.ModelAdmin):
    """Admin class for CurrencyConversion model."""

    list_filter = ("from_currency", "to_currency")
    search_fields = ("from_currency", "to_currency")
    list_display = ("from_currency", "to_currency", "count", "created_at")
    fieldsets = (
        (
            "Currency Information",
            {
                "fields": ("from_currency", "to_currency", "count"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def has_add_permission(self, request):
        """Returns False to disable add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Returns False to disable change permission."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Returns False to disable delete permission."""
        return False
