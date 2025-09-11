from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from utils.bases.base_test import BaseJWTAPITestCase

User = get_user_model()


class TokenTestCase(BaseJWTAPITestCase):
    def setUp(self):
        super().setUp()

        self.obtain_url = reverse("v1:account:tokens-obtain")
        self.refresh_url = reverse("v1:account:tokens-refresh")
        self.verify_url = reverse("v1:account:tokens-verify")
        self.blacklist_url = reverse("v1:account:tokens-blacklist")

        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.refresh_token_str = str(self.refresh_token)

    def test_obtain_token_valid_credentials(self):
        data = {
            "phone_number": self.user_phone_number,
            "password": self.user_password,
        }
        response = self.client.post(self.obtain_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIsNotNone(response.data["access"])
        self.assertIsNotNone(response.data["refresh"])

    def test_obtain_token_invalid_credentials(self):
        data = {
            "phone_number": "+989351886691",
            "password": "wrongpassword",
        }
        response = self.client.post(self.obtain_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            _("No active account found with the given credentials"),
        )

    def test_refresh_token_valid(self):
        new_refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(new_refresh)}
        response = self.client.post(self.refresh_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIsNotNone(response.data["access"])

    def test_refresh_token_invalid(self):
        data = {"refresh": "invalidtoken"}
        try:
            response = self.client.post(self.refresh_url, data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data["detail"], _("Token is invalid or expired"))
        except TokenError:
            pass

    def test_refresh_token_blacklisted(self):
        new_refresh = RefreshToken.for_user(self.user)
        refresh_str = str(new_refresh)

        self.client.post(self.blacklist_url, {"refresh": refresh_str})

        try:
            response = self.client.post(self.refresh_url, {"refresh": refresh_str})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn("blacklisted", str(response.data["detail"]).lower())
        except TokenError:
            pass

    def test_verify_token_valid(self):
        data = {"token": self.access_token}
        response = self.client.post(self.verify_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], _("Token is valid."))

    def test_verify_token_invalid(self):
        data = {"token": "invalidtoken"}
        try:
            response = self.client.post(self.verify_url, data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data["detail"], _("Token is invalid or expired"))
        except TokenError:
            pass

    def test_blacklist_token_valid(self):
        new_refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(new_refresh)}
        response = self.client.post(self.blacklist_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], _("Token blacklisted."))

    def test_blacklist_token_invalid(self):
        data = {"refresh": "invalidtoken"}
        try:
            response = self.client.post(self.blacklist_url, data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data["detail"], _("Token is invalid or expired"))
        except TokenError:
            pass

    def test_blacklist_token_already_blacklisted(self):
        new_refresh = RefreshToken.for_user(self.user)
        refresh_str = str(new_refresh)
        data = {"refresh": refresh_str}

        response1 = self.client.post(self.blacklist_url, data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        try:
            response2 = self.client.post(self.blacklist_url, data)
            self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn("blacklisted", str(response2.data["detail"]).lower())
        except TokenError:
            pass
