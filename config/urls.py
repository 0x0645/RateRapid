"""URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path("auth/", include(("raterapid.users.urls", "users"), namespace="users")),
    path("rate/", include(("raterapid.rate.urls", "rate"), namespace="rate")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
