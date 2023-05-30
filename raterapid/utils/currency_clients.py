"""RateRapid Utils : Currency APIs Clients."""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.dateparse import parse_datetime

logger = logging.getLogger(__name__)


class BaseCurrencyAPIClient(ABC):
    """Abstract Base Class for Currency API Clients."""

    def __init__(self, api_key: str, base_url: str):
        """
        Initializes the BaseCurrencyAPIClient.

        Args:
            api_key (str): The API key to use for requests.
            base_url (str): The base URL for the API.
        """
        self.api_key = api_key
        self.base_url = base_url

    @property
    @abstractmethod
    def get_latest_rates_endpoint(self) -> str:
        """Abstract method to get the endpoint for latest rates."""
        raise NotImplementedError

    @abstractmethod
    def pair_conversion_endpoint(self, base: str, target: str, amount: float) -> str:
        """Abstract method to get the endpoint for pair conversion."""
        raise NotImplementedError

    def request(self, url: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Sends a GET request to the given URL and returns the response status and content.

        On successful execution, a tuple (True, content) is returned,
        where 'content' is the parsed JSON response from the server.
        On failure, the method returns (False, {}).

        Args:
            url (str): The URL to send the GET request to.

        Returns:
            Tuple[bool, Dict[str, Any]]: Tuple containing a boolean status and response content.
                Status is True if request succeeded and False otherwise.
                Content is a JSON response from the API on success and an empty dict on failure.
        """
        try:
            logger.info(f"Sending request to {url}")
            response = requests.get(url)
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"An error occurred during the request: {req_err}")
        except json.JSONDecodeError as json_err:
            logger.error(f"An error occurred while parsing the response into JSON: {json_err}")
        return False, {}

    @abstractmethod
    def get_latest_rates(self) -> Tuple[bool, Dict[str, Any]]:
        """Abstract method to get the latest rates from the API."""
        raise NotImplementedError

    @abstractmethod
    def pair_conversion(self, base: str, target: str, amount: float) -> Tuple[bool, Optional[float]]:
        """Abstract method to convert an amount of money from one currency to another."""
        raise NotImplementedError


class EXChangeRateClient(BaseCurrencyAPIClient):
    """
    Exchange Rate API Client that extends BaseCurrencyAPIClient.

    Handles communication with the ExchangeRate API.
    For more details on the API, refer to the API Documentation at https://exchangerate-api.com/docs/
    """

    def __init__(self, api_key: str):
        """
        Initialize the ExchangeRate API client.

        Args:
            api_key (str): The API key for the ExchangeRate API.
        """
        base_url = "https://v6.exchangerate-api.com/v6"
        super().__init__(api_key, base_url)

    @property
    def get_latest_rates_endpoint(self) -> str:
        """
        Construct and return the endpoint URL for getting the latest rates.

        Returns:
            str: The endpoint URL.
        """
        return f"{self.base_url}/{self.api_key}/latest"

    def pair_conversion_endpoint(self, base: str, target: str, amount: float) -> str:
        """
        Construct and return the endpoint URL for converting one currency to another.

        Args:
            base (str): The base currency for conversion.
            target (str): The target currency for conversion.
            amount (float): The amount of base currency to be converted.

        Returns:
            str: The endpoint URL.
        """
        return f"{self.base_url}/{self.api_key}/pair/{base}/{target}/{amount}"

    def get_latest_rates(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Retrieves the latest currency exchange rates from the API.

        Returns:
            Tuple[bool, Dict[str, Any]]: A tuple containing a boolean status and response content.
                Status is True if request succeeded and False otherwise.
                Content is a JSON response from the API on success, and an empty dict on failure.
        """
        success, data = self.request(self.get_latest_rates_endpoint)
        return success, data.get("conversion_rates", {})

    def pair_conversion(self, base: str, target: str, amount: float) -> Tuple[bool, Optional[float]]:
        """
        Converts a specific amount of money from one currency (base) to another (target).

        Args:
            base (str): The base currency to convert from.
            target (str): The target currency to convert to.
            amount (float): The amount of base currency to be converted.

        Returns:
            Tuple[bool, Optional[float]]: A tuple containing a boolean status and conversion result.
                Status is True if request succeeded and False otherwise.
                The conversion result is a float representing the converted amount in target currency on success,
                and None on failure.
        """
        success, data = self.request(self.pair_conversion_endpoint(base, target, amount))
        return success, data.get("conversion_result")


class CurrencyLayerClient(BaseCurrencyAPIClient):
    """
    Currency Layer API Client that extends BaseCurrencyAPIClient.

    Handles communication with the CurrencyLayer API.
    For more details on the API, refer to the API Documentation at https://currencylayer.com/documentation
    """

    def __init__(self, api_key: str):
        """
        Initialize the CurrencyLayer API client.

        Args:
            api_key (str): The API key for the CurrencyLayer API.
        """
        base_url = "http://apilayer.net/api"
        super().__init__(api_key, base_url)

    @property
    def get_latest_rates_endpoint(self) -> str:
        """
        Construct and return the endpoint URL for getting the latest rates.

        Returns:
            str: The endpoint URL.
        """
        return f"{self.base_url}/live?access_key={self.api_key}"

    def _remove_usd_from_keys(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes 'USD' prefix from keys in the provided dictionary.

        Args:
            data (Dict[str, any]): A dictionary with 'USD' prefixed keys.

        Returns:
            Dict[str, any]: A new dictionary with 'USD' prefix removed from keys.
        """
        return {key.replace("USD", ""): value for key, value in data.items()}

    def pair_conversion_endpoint(self, base: str, target: str, amount: float) -> str:
        """
        Construct and return the endpoint URL for converting one currency to another.

        Args:
            base (str): The base currency for conversion.
            target (str): The target currency for conversion.
            amount (float): The amount of base currency to be converted.


        Returns:
            str: The endpoint URL.
        """
        return f"{self.base_url}/convert?access_key={self.api_key}&from={base}&to={target}&amount={amount}"

    def get_latest_rates(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Retrieves the latest currency exchange rates from the API.

        Returns:
            Tuple[bool, Dict[str, Any]]: A tuple containing a boolean status and response content.
                Status is True if request succeeded and False otherwise.
                Content is a JSON response from the API on success, and an empty dict on failure.
        """
        success, data = self.request(self.get_latest_rates_endpoint)
        return success, self._remove_usd_from_keys(data.get("quotes", {}))

    def pair_conversion(self, base: str, target: str, amount: float) -> Tuple[bool, Optional[float]]:
        """
        Converts a specific amount of money from one currency (base) to another (target).

        Args:
            base (str): The base currency to convert from.
            target (str): The target currency to convert to.
            amount (float): The amount of base currency to be converted.

        Returns:
            Tuple[bool, Optional[float]]: A tuple containing a boolean status and conversion result.
                Status is True if request succeeded and False otherwise.
                The conversion result is a float representing the converted amount in target currency on success,
                and None on failure.
        """
        success, data = self.request(self.pair_conversion_endpoint(base, target, amount))
        return success, data.get("result")


def compute_cross_rate(rate1: float, rate2: float) -> float:
    """
    Compute the cross exchange rate between two currencies relative to a common currency.

    Args:
        rate1: Exchange rate of first currency relative to common currency.
        rate2: Exchange rate of second currency relative to common currency.

    Returns:
        Cross-rate between the two currencies.
    """
    return rate2 / rate1


def get_cached_api_rates():
    """Retrieves the API rates data from the cache."""
    cached_data = cache.get("api_rates")

    if cached_data is not None:
        updated_at = parse_datetime(cached_data.get("updated_at"))

        return cached_data.get("rate"), updated_at

    return None, None


def get_latest_rates() -> Tuple[bool, Dict[str, Any]]:
    """
    Retrieves the latest currency exchange rates.

    Tries the ExchangeRate API first, then falls back to the CurrencyLayer API if the first one fails.


    Returns:
        Tuple[bool, Dict[str, Any]]: A tuple containing a boolean status and response content.
    """
    success, data = exchangerate_client.get_latest_rates()
    if not success:
        success, data = currencylayer_client.get_latest_rates()
    return success, data


def pair_conversion(base: str, target: str, amount: float) -> Tuple[bool, Optional[float], datetime]:
    """
    Converts a specific amount of money from one currency (base) to another (target).

    This function first tries to convert the currencies using the ExchangeRate API. If it fails, it falls back to
    the CurrencyLayer API. If that fails too, it tries to calculate the conversion rate using cached rates.

    Args:
        base (str): The base currency code (e.g. "USD").
        target (str): The target currency code (e.g. "EUR").
        amount (float): The amount of base currency to be converted.

    Returns:
        Tuple[bool, Optional[float], datetime]: A tuple containing a boolean status indicating the success of the
        conversion, the conversion result, and the datetime of the rate used for conversion.
    """
    success, result = exchangerate_client.pair_conversion(base, target, amount)
    print(success, result)
    if success:
        logger.info(f"Converted {amount} {base} to {target} using ExchangeRate API.")
        return success, result, timezone.now()

    success, result = currencylayer_client.pair_conversion(base, target, amount)
    if success:
        logger.info(f"Converted {amount} {base} to {target} using CurrencyLayer API.")
        return success, result, timezone.now()

    data, last_updated = get_cached_api_rates()
    if data and last_updated:
        cross_rate = compute_cross_rate(data[base], data[target])
        result = cross_rate * amount
        logger.info(f"Converted {amount} {base} to {target} using cached rates.")
        return True, result, last_updated

    logger.error(f"Failed to convert {amount} {base} to {target}.")
    return False, 0.0, timezone.now()


exchangerate_client = EXChangeRateClient(settings.EXCHANGERATE_API_KEY)
currencylayer_client = CurrencyLayerClient(settings.EXCHANGERATE_API_KEY)
