"""Test suite for views."""

from unittest import TestCase

from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase, force_authenticate

from raterapid.users.tests.factory import UserFactory
from raterapid.users.views import LoginView, RegenerateTokenView, SignUpView


class TestUserAPIViewsGenaric(TestCase):
    """Test cases for user API views as genaric python class."""

    def setUp(self):
        """Set up test environment."""
        self.factory = RequestFactory()
        self.user = UserFactory.create()
        self.user.set_password("testpassword")
        self.user.save()
        self.token = Token.objects.create(user=self.user)

    def test_SignUpView(self):
        """Test case for user sign up."""
        view = SignUpView.as_view()
        request = self.factory.post(
            "/signup/", {"username": "testuser", "password": "testpassword", "email": "testemail@gmail.com"}
        )
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_LoginView(self):
        """Test case for user login."""
        view = LoginView.as_view()
        request = self.factory.post("/login/")
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_RegenerateTokenView(self):
        """Test case for token regeneration."""
        view = RegenerateTokenView.as_view()
        request = self.factory.post("/regenerate_token/")
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertNotEqual(response.data["token"], self.token.key)
        self.assertEqual(response.status_code, 200)


class TestUserAPIViews(APITestCase):
    """Test cases for user API views."""

    def setUp(self):
        """Set up test environment."""
        self.client = APIClient()
        self.user = UserFactory.create()
        self.user.set_password("testpassword")
        self.user.save()
        self.token = Token.objects.create(user=self.user)

    def test_SignUpView_success(self):
        """Test case for successful user sign up."""
        url = reverse("users:signup")
        response = self.client.post(
            url, {"username": "testuser", "password": "testpassword", "email": "testemail@gmail.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_SignUpView_failure(self):
        """Test case for failed user sign up."""
        url = reverse("users:signup")
        response = self.client.post(
            url, {"username": "", "password": "testpassword", "email": "testemail@gmail.com"}  # Invalid username
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_LoginView_success(self):
        """Test case for successful user login."""
        url = reverse("users:login")
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_LoginView_failure(self):
        """Test case for failed user login (unauthenticated)."""
        url = reverse("users:login")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_RegenerateTokenView_success(self):
        """Test case for successful token regeneration."""
        url = reverse("users:regenerate_token")
        self.client.force_authenticate(user=self.user, token=self.token)
        response = self.client.post(url)
        self.assertNotEqual(response.data["token"], self.token.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_RegenerateTokenView_failure(self):
        """Test case for failed token regeneration (unauthenticated)."""
        url = reverse("users:regenerate_token")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
