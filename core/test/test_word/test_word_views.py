from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category, Word


class WordTestViews(TestCase):
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

        self.client = APIClient()

    def test_get_words(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/word/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_word(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/word/",
            {
                "word": "元気",
                "reading": "げんき",
                "meaning": "energetic",
                "type": "Substantivo",
                "level": "N5",
                "category": self.category.id,
                "created_by": self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_word_create_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/word/",
            {
                "word": "元気",
                "reading": "genki",
                "meaning": "energetic",
                "type": "Substantivo",
                "level": "N5",
                "category": self.category.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_word_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/word/{self.word.id}/", {"level": "N4"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_word_update_failed_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/word/{99999}/", {"level": "N4"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_word_update_failed_field_invalid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/word/{self.word.id}/", {"level": "N*"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_word(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/word/{self.word.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_word_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/word/{99999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_word(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/word/{self.word.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_word_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/word/{99999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
