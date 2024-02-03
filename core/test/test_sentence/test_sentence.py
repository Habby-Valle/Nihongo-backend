from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Grammar, Sentence


class SentenceViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.grammar = Grammar.objects.create(
            grammar="grammar",
            structure="あまり",
            level="N4",
            explain="teste",
            created_by=self.user,
        )
        self.sentence = Sentence.objects.create(
            sentence="あまり",
            translate="teste",
            annotation="teste",
            grammar=self.grammar,
            created_by=self.user,
        )

        self.client = APIClient()

    def test_sentence_list_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/sentence_list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sentence_create(self):
        data = {
            "sentence": "あまりあまり",
            "translate": "teste",
            "annotation": "teste",
            "grammar": self.grammar.id,
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/sentence/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sentence_create_failed(self):
        data = {
            "sentence": "",
            "translate": "teste",
            "annotation": "teste",
            "grammar": self.grammar.id,
            "created_by": self.user.id,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/sentence/", data=data, format="json")

        return self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sentence_detail_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/sentence/{self.sentence.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sentence_detail_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/sentence/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sentence_update(self):
        data = {
            "sentence": "あまりあまり",
            "translate": "teste",
            "annotation": "teste",
            "grammar": self.grammar.id,
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/sentence/{self.sentence.id}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sentence_update_field_failed(self):
        data = {
            "sentence": "",
            "translate": "teste",
            "annotation": "teste",
            "grammar": self.grammar.id,
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/sentence/{self.sentence.id}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sentence_update_not_found(self):
        data = {
            "sentence": "あまりあまり",
            "translate": "teste",
            "annotation": "teste",
            "grammar": self.grammar.id,
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/sentence/{999}/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sentence_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/sentence/{self.sentence.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_sentence_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/sentence/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
