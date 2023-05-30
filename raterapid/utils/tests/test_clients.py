"""Test cases for the currency_clients."""
from unittest.mock import patch

from django.test import TestCase
from requests import HTTPError

from ..currency_clients import CurrencyLayerClient, EXChangeRateClient, get_latest_rates, pair_conversion


class TestClients(TestCase):
    """Test cases for the currency_clients module."""

    def setUp(self):
        """Tests Setup."""
        self.ex_client = EXChangeRateClient("test")
        self.currencylayer_client = CurrencyLayerClient("test")

    @patch("requests.get")
    def test_get_latest_rates(self, mock_get):
        """Test getting latest rates for the EXChangeRateClient."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "base_code": "USD",
            "conversion_rates": {
                "EUR": 0.85,
                "GBP": 0.76,
                "AUD": 1.38,
            },
        }

        success, rates = self.ex_client.get_latest_rates()

        self.assertTrue(success)
        self.assertEqual(rates["EUR"], 0.85)
        self.assertEqual(rates["GBP"], 0.76)
        self.assertEqual(rates["AUD"], 1.38)

    @patch("requests.get")
    def test_pair_conversion(self, mock_get):
        """Test pair conversion for the EXChangeRateClient."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "base_code": "USD",
            "target_code": "EUR",
            "conversion_rate": 0.85,
            "conversion_result": 85.0,
        }

        success, conversion_result = self.ex_client.pair_conversion("USD", "EUR", 100)

        self.assertTrue(success)
        self.assertEqual(conversion_result, 85.0)

    @patch("requests.get")
    def test_get_latest_rates_api_request_failure(self, mock_get):
        """Test failing scenario for get_latest_rates method for the EXChangeRateClient."""
        mock_get.side_effect = HTTPError()

        success, rates = self.ex_client.get_latest_rates()

        self.assertFalse(success)
        self.assertEqual(rates, {})

    @patch("requests.get")
    def test_pair_conversion_api_request_failure(self, mock_get):
        """Test failing scenario for pair_conversion method for the EXChangeRateClient."""
        mock_get.side_effect = HTTPError()

        success, result = self.ex_client.pair_conversion("USD", "EUR", 100)

        self.assertFalse(success)
        self.assertIsNone(result)

    @patch("requests.get")
    def test_currencylayer_get_latest_rates(self, mock_get):
        """Test getting latest rates for the CurrencyLayerClient."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "base_code": "USD",
            "quotes": {
                "EUR": 0.85,
                "GBP": 0.76,
                "AUD": 1.38,
            },
        }

        success, rates = self.currencylayer_client.get_latest_rates()

        self.assertTrue(success)
        self.assertEqual(rates["EUR"], 0.85)
        self.assertEqual(rates["GBP"], 0.76)
        self.assertEqual(rates["AUD"], 1.38)

    @patch("requests.get")
    def test_currencylayer_pair_conversion(self, mock_get):
        """Test pair conversion for the CurrencyLayerClient."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "base_code": "USD",
            "target_code": "EUR",
            "conversion_rate": 0.85,
            "result": 85.0,
        }

        success, conversion_result = self.currencylayer_client.pair_conversion("USD", "EUR", 100)

        self.assertTrue(success)
        self.assertEqual(conversion_result, 85.0)

    @patch("requests.get")
    def test_currencylayer_get_latest_rates_api_request_failure(self, mock_get):
        """Test failing scenario for get_latest_rates method for the CurrencyLayerClient."""
        mock_get.side_effect = HTTPError()

        success, rates = self.currencylayer_client.get_latest_rates()

        self.assertFalse(success)
        self.assertEqual(rates, {})

    @patch("requests.get")
    def test_currencylayer_pair_conversion_api_request_failure(self, mock_get):
        """Test failing scenario for pair_conversion method for the CurrencyLayerClient."""
        mock_get.side_effect = HTTPError()

        success, result = self.currencylayer_client.pair_conversion("USD", "EUR", 100)

        self.assertFalse(success)
        self.assertIsNone(result)

    @patch.object(EXChangeRateClient, "get_latest_rates")
    @patch.object(CurrencyLayerClient, "get_latest_rates")
    def test_get_latest_rates_fallback(self, mock_currencylayer_rates, mock_exchangerate_rates):
        """Test fallback to CurrencyLayerClient when getting latest rates from EXChangeRateClient fails."""
        mock_exchangerate_rates.return_value = (False, {})
        mock_currencylayer_rates.return_value = (True, {"USD": 1.0, "EUR": 0.85})

        success, rates = get_latest_rates()

        self.assertTrue(success)
        self.assertEqual(rates, {"USD": 1.0, "EUR": 0.85})

    @patch.object(EXChangeRateClient, "pair_conversion")
    @patch.object(CurrencyLayerClient, "pair_conversion")
    def test_pair_conversion_fallback(self, mock_currencylayer_conversion, mock_exchangerate_conversion):
        """Test fallback to CurrencyLayerClient when pair conversion from EXChangeRateClient fails."""
        mock_exchangerate_conversion.return_value = (False, None)
        mock_currencylayer_conversion.return_value = (True, 85.0)

        success, result, _ = pair_conversion("USD", "EUR", 100)

        self.assertTrue(success)
        self.assertEqual(result, 85.0)
