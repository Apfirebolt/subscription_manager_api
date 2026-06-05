from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import CustomUser


class AuthAPITests(APITestCase):
    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "strongpassword"
        self.user = CustomUser.objects.create_user(email=self.email, password=self.password, username="tester")

    def test_token_obtain_and_profile(self):
        # Obtain token
        url = reverse("api:signin")
        resp = self.client.post(url, {"email": self.email, "password": self.password}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

        access = resp.data["access"]

        # Access profile
        profile_url = reverse("api:me")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        profile_resp = self.client.get(profile_url)
        self.assertEqual(profile_resp.status_code, 200)
        self.assertEqual(profile_resp.data.get("email"), self.email)

    def test_register_endpoint_creates_user(self):
        url = reverse("api:signup")
        payload = {"email": "newuser@example.com", "username": "newuser", "password": "newstrongpass"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())
