from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from predictor.models import PredictionHistory


class PredictorViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testdoctor",
            password="TestPassword123!"
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancer Risk Intelligence System")

    def test_login_redirect_for_protected_views(self):
        dashboard_url = reverse("dashboard")
        response = self.client.get(dashboard_url)
        self.assertRedirects(response, f"/accounts/login/?next={dashboard_url}")

    def test_authenticated_dashboard_view(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdoctor")

    def test_authenticated_predict_view_get(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        response = self.client.get(reverse("predict"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancer Risk Prediction Assessment")

    def test_authenticated_analytics_view(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        response = self.client.get(reverse("analytics"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clinical Analytics")

    def test_authenticated_history_view(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prediction History Logs")
