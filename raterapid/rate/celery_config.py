# coding=utf-8
"""Rate App Celery-Config."""


from celery.schedules import crontab
from django.conf import settings


class RateAppCeleryConfig(object):
    """Class representing the Rate application celery configuration."""

    @staticmethod
    def beat_schedule() -> dict:
        """Retrieve the celery.beat_schedule records related to the App."""
        return {
            "schedule-cache_api_rates": {
                "task": "raterapid.rate.tasks.cache_api_rates",
                "schedule": crontab(**settings.CACHE_API_RATE),
                "args": (),
            },
        }


__all__ = ["RateAppCeleryConfig"]
