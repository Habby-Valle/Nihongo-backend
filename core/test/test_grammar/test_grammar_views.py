from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Grammar


class GrammarViewsTest(TestCase):
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
        self.client = APIClient()

    def test_grammar_list_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/grammar/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_grammar_create(self):
        data = {
            "grammar": "gammar teste",
            "structure": "あまり~",
            "level": "N4",
            "explain": "Texto longo",
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/grammar/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_grammar_create_failed(self):
        data = {
            "grammar": "gammar teste",
            "structure": "",
            "level": "N4",
            "explain": "Texto longo",
            "created_by": self.user.id,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/grammar/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_grammar_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/grammar/{self.grammar.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["grammar"]["grammar"], self.grammar.grammar)
        self.assertEqual(response.data["grammar"]["structure"], self.grammar.structure)
        self.assertEqual(response.data["grammar"]["level"], self.grammar.level)
        self.assertEqual(response.data["grammar"]["explain"], self.grammar.explain)
        self.assertEqual(
            response.data["grammar"]["created_by"], self.grammar.created_by.id
        )

    def test_grammar_detail_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/grammar/{9999999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grammar_update_put(self):
        data = {
            "grammar": "gammar teste novo",
            "structure": "あまり~",
            "level": "N4",
            "explain": "Texto longo longo",
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            f"/api/grammar/{self.grammar.pk}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["grammar"]["grammar"], data["grammar"])
        self.assertEqual(response.data["grammar"]["structure"], data["structure"])
        self.assertEqual(response.data["grammar"]["level"], data["level"])
        self.assertEqual(response.data["grammar"]["explain"], data["explain"])

    def test_grammar_updated_invalid_pk_put(self):
        data = {
            "grammar": "gammar teste novo",
            "structure": "あまり~",
            "level": "N4",
            "explain": "Texto longo longo",
            "created_by": self.user.id,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(f"/api/grammar/{9999}/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grammar_update_invalid_field_put(self):
        data = {
            "grammar": "gammar teste novo",
            "structure": "",
            "level": "N4",
            "explain": "Texto longo longo",
            "created_by": self.user.id,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            f"/api/grammar/{self.grammar.pk}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_grammar_update_patch(self):
        data = {"grammar": "grammar new"}

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/grammar/{self.grammar.pk}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["grammar"]["grammar"], data["grammar"])

    def test_grammar_updated_invalid_pk_patch(self):
        data = {"structure": ""}

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/grammar/{9999}/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_grammar_update_invalid_field_patch(self):
        data = {"structure": ""}

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/grammar/{self.grammar.pk}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_grammar_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/grammar/{self.grammar.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Grammar.objects.count(), 0)

    def test_grammar_delete_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/grammar/{9999999}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Grammar.objects.count(), 1)
