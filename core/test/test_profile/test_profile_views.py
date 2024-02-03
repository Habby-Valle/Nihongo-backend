from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ProfileViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            first_name="testuser firstname",
            last_name="testuserlastname",
            password="testpassword",
        )
        self.client = APIClient()

    def test_update_profile(self):
        data = {"phone": "84999999996"}

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/profile/{self.user.pk}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["phone"], data["phone"])

    def test_update_profile_not_found(self):
        data = {"phone": "84999999996"}

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/profile/{9999}/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_profile_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/profile/{self.user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/profile/{9999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
