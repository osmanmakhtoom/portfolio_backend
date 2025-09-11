from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

from utils.bases.base_test import BaseJWTAPITestCase

User = get_user_model()


class UserTestCase(BaseJWTAPITestCase):
    def setUp(self):
        super(UserTestCase, self).setUp()

        self.users_url = reverse("v1:account:users-list")
        self.me_url = reverse("v1:account:users-me")
        self.register_url = reverse("v1:account:users-register")
        self.reset_password_url = reverse("v1:account:users-reset-password")
        self.add_address_url = reverse("v1:account:users-add-address")
        self.edit_profile_url = reverse("v1:account:users-edit-profile")

    def test_list_users_as_admin(self):
        self._authenticate_admin()
        print({
            'client': self.client.__dict__
        })
        response = self.client.get(self.users_url)
        print({
            'response': response.__dict__
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_users_as_regular_user(self):
        self._authenticate_user()
        print({
            'client': self.client.__dict__
        })
        response = self.client.get(self.users_url)
        print({
            'response': response.__dict__
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_unauthenticated(self):
        print({
            'client': self.client.__dict__
        })
        response = self.client.get(self.users_url)
        print({
            'response': response.__dict__
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_as_admin(self):
        self._authenticate_admin()
        url = f"{self.users_url}/{self.user.id}"
        print({
            'client': self.client.__dict__
        })
        response = self.client.get(url)
        print({
            'response': response.__dict__
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], self.user.phone_number)

    def test_retrieve_user_as_regular_user(self):
        self._authenticate_user()
        url = f"{self.users_url}/{self.user.id}"
        print({
            'client': self.client.__dict__
        })
        response = self.client.get(url)
        print({
            'response': response.__dict__
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_action_authenticated(self):
        self._authenticate_user()
        print({
            'client': self.client.__dict__
        })
        response = self.client.get(self.me_url)
        print({
            'response': response.__dict__
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], self.user.phone_number)

    def test_me_action_unauthenticated(self):
        print({
            'client': self.client.__dict__
        })
        response = self.client.get(self.me_url)
        print({
            'response': response.__dict__
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_user(self):
        data = {
            "phone_number": "+989351886691",
            "password": "newpass123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone_number="+989351886691").exists())

    def test_register_user_invalid_data(self):
        data = {
            "phone_number": "",
            "email": "invalid",
            "password": "short",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_as_admin(self):
        self._authenticate_admin()
        data = {"new_password": "newpassword123"}
        response = self.client.post(
            f"{self.reset_password_url}?user_id={self.user.id}", data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_reset_password_missing_params(self):
        self._authenticate_user()
        response = self.client.post(self.reset_password_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reset_password_as_regular_user(self):
        self._authenticate_user()
        response = self.client.post(self.reset_password_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_address_authenticated(self):
        self._authenticate_user()
        data = {
            "street": "123 Main St",
            "city": "Anytown",
            "province": "CA",
            "postal_code": "12345",
            "country": "US",
        }
        response = self.client.post(self.add_address_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["street"], "123 Main St")

    def test_add_address_unauthenticated(self):
        data = {
            "street": "123 Main St",
            "city": "Anytown",
            "province": "CA",
            "postal_code": "12345",
            "country": "US",
        }
        response = self.client.post(self.add_address_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_profile_authenticated(self):
        self._authenticate_user()
        data = {"bio": "Updated"}
        response = self.client.patch(self.edit_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.userprofile.bio, "Updated")

    def test_edit_profile_unauthenticated(self):
        data = {"bio": "Updated"}
        response = self.client.patch(self.edit_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_as_admin(self):
        self._authenticate_admin()
        url = f"{self.users_url}/{self.user.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_delete_user_as_regular_user(self):
        self._authenticate_user()
        url = f"{self.users_url}/{self.user.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_disallowed(self):
        self._authenticate_user()
        data = {"phone_number": "+989113190123", "password": "pass"}
        response = self.client.post(self.users_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_disallowed(self):
        self._authenticate_user()
        url = f"{self.users_url}/{self.user.id}"
        data = {"phone_number": "+989113190123"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_disallowed(self):
        self._authenticate_user()
        url = f"{self.users_url}/{self.user.id}"
        data = {"phone_number": "+989113190123"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
