# coding=utf-8
"""User App URLS."""
from django.urls import path

from .views import LoginView, RegenerateTokenView, SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("get-token/", LoginView.as_view(), name="login"),
    path("regenerate-token/", RegenerateTokenView.as_view(), name="regenerate_token"),
]
