# coding=utf-8
"""USER App Views."""
import logging

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class SignUpView(APIView):
    """User Registration API."""

    permission_classes = [AllowAny]

    def post(self, request):
        """API POST HTTP method."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            logger.info(f"User {user.username} registered successfully.")
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)

        logger.warning(f"User registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User Login API."""

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """API POST HTTP method."""
        token, _ = Token.objects.get_or_create(user=request.user)
        logger.info(f"User {request.user.username} logged in successfully.")
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class RegenerateTokenView(APIView):
    """API to regenerate user token."""

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """API POST HTTP method."""
        self.regenerate_token(request.user)
        return Response({"token": request.user.auth_token.key}, status=status.HTTP_200_OK)

    @staticmethod
    def regenerate_token(user):
        """Deletes the old token for a user and generates a new one."""
        Token.objects.filter(user=user).delete()
        logger.info(f"Old token for user {user.username} deleted.")
        Token.objects.create(user=user)
        logger.info(f"New token generated for user {user.username}.")
