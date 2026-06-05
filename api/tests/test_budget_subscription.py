from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import CustomUser
from subscriptions.models import Service, Budget
import datetime


class BudgetSubscriptionAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="buduser@example.com", password="budpass123", username="bud")
        self.other = CustomUser.objects.create_user(email="other@example.com", password="otherpass", username="other")
        self.service = Service.objects.create(name="Spotify", logo_url="http://s", is_approved=True)

    def auth_client(self, email, password):
        login_url = reverse("api:signin")
        resp = self.client.post(login_url, {"email": email, "password": password}, format="json")
        token = resp.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_subscription_requires_budget(self):
        # authenticate user without a budget
        self.auth_client("buduser@example.com", "budpass123")

        url = reverse("api:subscriptions")
        payload = {
            "service": self.service.id,
            "cost": "9.99",
            "billing_cycle": "MONTHLY",
            "next_billing_date": datetime.date.today().isoformat(),
        }

        resp = self.client.post(url, payload, format="json")
        # Should fail because no budget exists
        self.assertEqual(resp.status_code, 400)
        self.assertIn("budget", str(resp.data))

        # create a budget and retry
        budgets_url = reverse("api:budgets")
        bpayload = {"amount": "100.00", "duration": "MONTHLY", "description": "my budget"}
        bresp = self.client.post(budgets_url, bpayload, format="json")
        self.assertEqual(bresp.status_code, 201)

        # retry subscription
        resp2 = self.client.post(url, payload, format="json")
        self.assertEqual(resp2.status_code, 201)

    def test_budget_list_only_user_budgets(self):
        # create budgets for both users
        Budget.objects.create(user=self.user, amount=50, duration="MONTHLY")
        Budget.objects.create(user=self.other, amount=75, duration="MONTHLY")

        self.auth_client("buduser@example.com", "budpass123")
        url = reverse("api:budgets")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # API may return paginated responses; normalize to a list
        if isinstance(resp.data, dict) and "results" in resp.data:
            data_list = resp.data["results"]
        else:
            data_list = resp.data

        # API should return the same number of budgets as exist for this user
        from subscriptions.models import Budget as _Budget
        expected = _Budget.objects.filter(user=self.user).count()
        self.assertEqual(len(data_list), expected)
