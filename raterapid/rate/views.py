# coding=utf-8
"""Rate App views."""

import logging
from datetime import datetime
from typing import Dict, Optional, Tuple

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from raterapid.utils.currency_clients import pair_conversion

from .models import CurrencyConversion
from .serializers import CurrencyConversionResponseSerializer, CurrencyConversionSerializer

logger = logging.getLogger(__name__)


class CurrencyConversionView(APIView):
    """API to convert between two currencies."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """API POST HTTP method."""
        serializer = CurrencyConversionSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error(f"Currency conversion failed. Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        from_currency = serializer.validated_data["from_currency"]
        to_currency = serializer.validated_data["to_currency"]
        amount = serializer.validated_data["amount"]

        converted_amount, last_updated = self.convert_currency(from_currency, to_currency, amount)
        if converted_amount is None or last_updated is None:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"message": "Internal server error it is us not you."},
            )
        response_data = self.create_response_data(from_currency, to_currency, float(converted_amount), last_updated)

        return self.create_response(response_data)

    @staticmethod
    def convert_currency(
        from_currency: str, to_currency: str, amount: float
    ) -> Tuple[Optional[float], Optional[datetime]]:
        """
        Converts an amount from one currency to another.

        Args:
            from_currency (str): The base currency code (e.g. "USD").
            to_currency (str): The target currency code (e.g. "EUR").
            amount (float): The amount of base currency to be converted.

        Returns:
            Tuple[Optional[float], Optional[datetime]]: A tuple containing the converted amount and the last updated
            time of the rates used for conversion.
        """
        success, converted_amount, last_updated = pair_conversion(from_currency, to_currency, amount)
        if not success:
            return None, None
        CurrencyConversion.get_or_increment(from_currency, to_currency)
        logger.info(f"Converted {amount} from {from_currency} to {to_currency}. Result: {converted_amount}")
        return converted_amount, last_updated

    @staticmethod
    def create_response_data(
        from_currency: str, to_currency: str, converted_amount: float, last_updated: datetime
    ) -> Dict:
        """
        Creates the response data to be returned by the API.

        Args:
            from_currency (str): The base currency code (e.g. "USD").
            to_currency (str): The target currency code (e.g. "EUR").
            converted_amount (float): The amount of target currency resulted from the conversion.
            last_updated (datetime): The last updated time of the rates used for conversion.

        Returns:
            Dict: A dictionary containing the response data.
        """
        return {
            "last_updated": last_updated,
            "amount": converted_amount,
            "base": from_currency,
            "target": to_currency,
        }

    def create_response(self, response_data: Dict) -> Response:
        """
        Creates a Response object to be returned by the API.

        Args:
            response_data (Dict): The data to be included in the response.

        Returns:
            Response: A Response object containing the serialized response data.
            In case of serialization failure, it returns an error response.
        """
        response_serializer = CurrencyConversionResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.validated_data, status=status.HTTP_200_OK)

        logger.error(f"Response serialization failed. Errors: {response_serializer.errors}")
        return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
