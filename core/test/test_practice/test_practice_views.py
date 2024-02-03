from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Grammar, PracticeGrammar


class PracticeGrammarViewsTest(TestCase):
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

        self.practice_grammar = PracticeGrammar.objects.create(
            grammar=self.grammar,
            first_sentence="あまり",
            second_sentence="あまり",
            third_sentence="あまり",
            created_by=self.user,
        )
        self.client = APIClient()

    def test_practice_grammar_list_get(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/sentence_list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_practice_grammar_create(self):
        data = {
            "grammar": self.grammar.id,
            "first_sentence": "あまり",
            "second_sentence": "あまり",
            "third_sentence": "あまり",
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/choice_grammar/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_practice_grammar_create_failed(self):
        data = {
            "grammar": self.grammar.id,
            "first_sentence": "",
            "second_sentence": "あまり",
            "third_sentence": "あまり",
            "created_by": self.user.id,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/choice_grammar/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_practice_grammar_update(self):
        data = {
            "grammar": self.grammar.id,
            "first_sentence": "あまり",
            "second_sentence": "あまり",
            "third_sentence": "あまり",
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/choice_grammar/{self.practice_grammar.id}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_practice_grammar_update_failed(self):
        data = {
            "grammar": self.grammar.id,
            "first_sentence": "",
            "second_sentence": "あまり",
            "third_sentence": "あまり",
            "created_by": self.user.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/choice_grammar/{self.practice_grammar.id}/", data=data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_practice_grammar_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            f"/api/choice_grammar/{self.practice_grammar.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_practice_grammar_delete_failed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/choice_grammar/{9999999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_chosen_grammar(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/choice_grammar/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
