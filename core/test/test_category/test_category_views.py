from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category


class CategoryTestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.category = Category.objects.create(
            name="testcategory", is_created_by_user=False, created_by=self.user
        )

        self.client = APIClient()

    def test_category_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/category/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/category/", {"name": "categorytest", "is_created_by_user": True}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_created_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/category/", {"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/category/{self.category.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/category/{9999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/category/{self.category.pk}/", {"name": "testcategoryupdate"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_update_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/category/{self.category.pk}/", {"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/category/{self.category.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_category_delete_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/category/{9999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
