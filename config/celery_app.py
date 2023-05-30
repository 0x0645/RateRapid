# coding=utf-8
"""
This file contains Implementation of Celery App object for the Raterapid project.

Helpful links:
    - https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
import os
import logging
from celery import Celery
from celery.signals import setup_logging
from raterapid.rate.celery_config import RateAppCeleryConfig

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("raterapid")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {}
app.conf.beat_schedule.update(RateAppCeleryConfig.beat_schedule())


@setup_logging.connect
def setup_celery_logging(**kwargs):
    """Set celery worker ROOT logger to celery."""
    return logging.getLogger("celery")
