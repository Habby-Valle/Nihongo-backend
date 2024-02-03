from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category, Example, Word


class ExampleTestsViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.category = Category.objects.create(
            name="testcategory", is_created_by_user=False, created_by=self.user
        )
        self.word = Word.objects.create(
            word="見える",
            reading="みえる",
            meaning="to be seen",
            type="Verbo - Grupo 1",
            level="N5",
            category=self.category,
            created_by=self.user,
        )
        self.example = Example.objects.create(
            example="私は見える",
            reading="わたしはみえる",
            meaning="I can see",
            annotation="Teste",
            word=self.word,
            created_by=self.user,
        )
        self.client = APIClient()

    def test_example_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/example/{self.word.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_example_list_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/example/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f"/api/example/{self.word.id}/",
            {
                "example": "私は見える",
                "reading": "わたしはみえる",
                "meaning": "I can see",
                "annotation": "Teste",
                "word": self.word.id,
                "created_by": self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_example_create_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f"/api/example/{9999}/",
            {
                "example": "私は見える",
                "reading": "わたしはみえる",
                "meaning": "I can see",
                "annotation": "Teste",
                "word": self.word.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_create_invalid_field(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f"/api/example/{self.word.id}/",
            {
                "example": "Watashi wa mieru",
                "reading": "わたしはみえる",
                "meaning": "I can see",
                "annotation": "Teste",
                "word": self.word.id,
                "created_by": self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_example_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f"/api/example_detail/{self.word.id}/{self.example.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_example_get_word_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/example_detail/{999}/{self.example.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_get_example_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/example_detail/{self.word.id}/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_get_word_id_and_example_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/example_detail/{999}/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/example_detail/{self.word.id}/{self.example.id}/",
            {"example": "私は見える"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_example_update_word_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/example_detail/{999}/{self.example.id}/", {"example": "私は見える"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_update_example_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/example_detail/{self.word.id}/{999}/", {"example": "私は見える"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_update_word_id_and_example_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/example_detail/{999}/{999}/", {"example": "私は見える"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_update_invalid_field(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/example_detail/{self.word.id}/{self.example.id}/",
            {"example": "Watashi wa mieru"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_example_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            f"/api/example_detail/{self.word.id}/{self.example.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_example_delete_word_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/example_detail/{999}/{self.example.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_delete_example_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/example_detail/{self.word.id}/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_example_delete_word_id_and_example_id_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/example_detail/{999}/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
