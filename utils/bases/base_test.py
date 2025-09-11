from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


User = get_user_model()


class BaseJWTAPITestCase(TestCase):
    jwt_obtain_pair_url = "v1:account:tokens-obtain"

    @classmethod
    def setUpTestData(cls):
        cls.admin_phone_number = "+989113190153"
        cls.admin_password = "password123"

        cls.user_phone_number = "+989113190154"
        cls.user_password = "password456"

        cls.admin = User.objects.create_superuser(
            phone_number=cls.admin_phone_number,
            password=cls.admin_password,
        )
        cls.user = User.objects.create_user(
            phone_number=cls.user_phone_number,
            password=cls.user_password,
        )

    def setUp(self):
        self.client = APIClient()

    def __authenticate(self, phone_number, password):
        url = reverse(self.jwt_obtain_pair_url)
        response = self.client.post(
            url,
            {"phone_number": phone_number, "password": password},
            format="json",
        )
        self.assertEqual(
            response.status_code, 200, f"JWT token request failed. {response.json()}"
        )
        return response.data["access"]

    def _authenticate_admin(self):
        access_token = self.__authenticate(self.admin_phone_number, self.admin_password)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def _authenticate_user(self):
        access_token = self.__authenticate(self.user_phone_number, self.user_password)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def tearDown(self):
        pass
