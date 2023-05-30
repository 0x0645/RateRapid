"""Rate App Task."""

from django.core.cache import cache
from django.utils import timezone

from config import celery_app as app
from raterapid.utils.currency_clients import get_latest_rates


@app.task(bind=True, max_retries=3)
def cache_api_rates(self):
    """Caches the API rates."""
    try:
        success, data = get_latest_rates()
        if success:
            cache.set("api_rates", {"rate": data, "updated_at": str(timezone.now())}, timeout=None)
            return (True, "Task Updated Data Successfully")
        return (False, "Task Failed to Update Data")
    except Exception as e:
        self.retry(exc=e, max_retries=3)
        return (False, "Task Failed to Update Data")
