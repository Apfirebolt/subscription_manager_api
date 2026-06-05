from django.urls import reverse
from rest_framework.test import APITestCase
from subscriptions.models import Service
from users.models import CustomUser


class ServiceAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="svcuser@example.com", password="pass12345", username="svc")
        # create a public service
        self.service = Service.objects.create(name="Netflix", logo_url="http://example.com/logo.png", is_approved=True)

    def test_list_services_public(self):
        url = reverse("api:services")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # Handle optional pagination
        if isinstance(data, dict) and "results" in data:
            data_list = data["results"]
        else:
            data_list = data

        # Expect at least the service we created
        names = [s["name"] for s in data_list]
        self.assertIn("Netflix", names)

    def test_create_service_requires_auth(self):
        url = reverse("api:services")
        payload = {"name": "MyCustomService", "logo_url": "http://example.com/myservice.png", "description": "desc"}
        # without auth
        resp = self.client.post(url, payload, format="json")
        self.assertIn(resp.status_code, (401, 403))

        # with auth
        login_url = reverse("api:signin")
        login = self.client.post(login_url, {"email": "svcuser@example.com", "password": "pass12345"}, format="json")
        access = login.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        resp2 = self.client.post(url, payload, format="json")
        self.assertEqual(resp2.status_code, 201, msg=f"status={resp2.status_code} data={getattr(resp2, 'data', resp2.content)}")
        self.assertTrue(Service.objects.filter(name="MyCustomService").exists())
