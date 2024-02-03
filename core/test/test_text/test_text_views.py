from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Text


class TextTestsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.text = Text.objects.create(
            title="神のイタズラ",
            text="""
                    ある日、神様が、人間の世界を見ていました。
                    すると、人間たちが、いろいろなことで、争っているのが見えました。
                    神様は、人間たちに、争いをやめるように、言いました。
                """,
            annotation="teste",
            created_by=self.user,
        )

        self.client = APIClient()

    def test_text_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/text/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_text_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/text/",
            {
                "title": "神のイタズラ",
                "text": """
                    ある日、神様が、人間の世界を見ていました。
                    すると、人間たちが、いろいろなことで、争っているのが見えました。
                    神様は、人間たちに、争いをやめるように、言いました。
                """,
                "annotation": "teste",
                "created_by": self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_text_create_invalid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/text/",
            {"title": "", "text": "", "annotation": "", "created_by": self.user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_text_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/text/{self.text.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_text_detail_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/text/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_text_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/text/{self.text.id}/",
            {
                "title": "神のイタズラ",
                "text": """
                    ある日、神様が、人間の世界を見ていました。
                    すると、人間たちが、いろいろなことで、争っているのが見えました。
                    神様は、人間たちに、争いをやめるように、言いました。
                """,
                "annotation": "teste",
                "created_by": self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_text_update_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/text/{999}/",
            {
                "title": "神のイタズラ",
                "text": """
                    ある日、神様が、人間の世界を見ていました。
                    すると、人間たちが、いろいろなことで、争っているのが見えました。
                    神様は、人間たちに、争いをやめるように、言いました。
                """,
                "annotation": "teste",
                "created_by": self.user.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_text_update_invalid(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/api/text/{self.text.id}/",
            {"title": "", "text": "", "annotation": "", "created_by": self.user.id},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_text_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/text/{self.text.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_text_delete_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/text/{999}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
