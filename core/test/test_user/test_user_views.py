from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class UserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            first_name="testuser firstname",
            last_name="testuserlastname",
            password="testpassword",
        )

        self.client = APIClient()

    def test_user_lis_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_register(self):
        data = {
            "username": "test_user",
            "email": "testuser@gmail.com",
            "first_name": "test firstname",
            "last_name": "test lastname",
            "password": "Password1!",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/user/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_register_failed(self):
        data = {
            "username": "",
            "email": "testuser@gmail.com",
            "first_name": "test firstname",
            "last_name": "test lastname",
            "password": "Password1!",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/user/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/user/{self.user.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], self.user.username)
        self.assertEqual(response.data["user"]["email"], self.user.email)
        self.assertEqual(response.data["user"]["first_name"], self.user.first_name)
        self.assertEqual(response.data["user"]["last_name"], self.user.last_name)

    def test_list_user_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/user/{99999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        data = {
            "username": "new_username",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/user/{self.user.pk}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], data["username"])

    def test_update_user_invalid_field(self):
        data = {"username": ""}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/user/{self.user.pk}/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_invalid_pk(self):
        data = {
            "username": "new_username",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/user/{9999}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/user/{self.user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/user/{9999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
