from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category, Conjugation, Word


class ConjugationTestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.category = Category.objects.create(
            name="testcategory", is_created_by_user=False, created_by=self.user
        )
        self.word_second = Word.objects.create(
            word="食べる",
            reading="たべる",
            meaning="to eat",
            type="Verbo - Grupo 2",
            level="N4",
            category=self.category,
            created_by=self.user,
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
        self.conjugation = Conjugation.objects.create(
            word=self.word,
            present="見える",
            past="見えた",
            negative="見えない",
            te_form="見えて",
            potential="見える",
            imperative="見えろ",
            passive="見えられる",
            causative="見えさせる",
            volitional="見えよう",
            created_by=self.user,
        )

        self.client = APIClient()

    def test_get_conjugation(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/conjugation/{self.word.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_conjugation_not_found(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/conjugation/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_conjugation_not_found(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(f"/api/conjugation/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_conjugation(self):
        self.client.force_authenticate(self.user)
        data = {
            "present": "見える",
        }
        response = self.client.patch(
            f"/api/conjugation_detail/{self.conjugation.id}/", data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_conjugation_not_found(self):
        self.client.force_authenticate(self.user)
        data = {
            "present": "見える",
        }
        response = self.client.patch(f"/api/conjugation_detail/{999}/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_conjugation_invalid_field(self):
        self.client.force_authenticate(self.user)
        data = {
            "present": "",
        }
        response = self.client.patch(
            f"/api/conjugation_detail/{self.conjugation.id}/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_conjugation(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(f"/api/conjugation_detail/{self.conjugation.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_conjugation_not_found(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(f"/api/conjugation_detail/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
