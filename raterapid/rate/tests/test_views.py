"""Test suite for views."""
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

from ..views import CurrencyConversionView


class CurrencyConversionViewTestCase(TestCase):
    """Test suite for CurrencyConversionView."""

    def setUp(self):
        """Set Up Method."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test", email="test@example.com", password="test")  # NOQA: S106
        self.token = Token.objects.create(user=self.user)
        self.view = CurrencyConversionView.as_view()

    @patch("raterapid.rate.views.CurrencyConversionView.convert_currency")
    def test_currency_conversion_successful(self, mock_convert):
        """Test for successful currency conversion."""
        mock_convert.return_value = (80.0, "2023-06-30")  # Mocked conversion result

        request = self.factory.post(
            reverse("rate:conversion"), {"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        )
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("amount", response.data)
        self.assertEqual(response.data["amount"], 80.0)  # Asserting the mocked result

    @patch("raterapid.rate.views.CurrencyConversionView.convert_currency")
    def test_currency_conversion_failure(self, mock_convert):
        """Test for failed currency conversion due to invalid data."""
        mock_convert.return_value = None  # Mocked conversion result

        request = self.factory.post(
            reverse("rate:conversion"),
            {"from_currency": "USD", "to_currency": "XYZ", "amount": 100},  # Invalid currency
        )
        force_authenticate(request, user=self.user, token=self.token)
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_currency_conversion_unauthenticated(self):
        """Test for unauthenticated currency conversion request."""
        request = self.factory.post(
            reverse("rate:conversion"), {"from_currency": "USD", "to_currency": "EUR", "amount": 100}
        )
        response = self.view(request)
        self.assertEqual(response.status_code, 401)  # HTTP_401_UNAUTHORIZED
