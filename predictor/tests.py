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

    def test_authenticated_risk_assessment_view_get(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        response = self.client.get(reverse("risk_assessment"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Module 1: Cancer Risk Assessment")

    def test_risk_assessment_form_submission(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        payload = {
            "patient_name": "Jane Doe",
            "age": 45,
            "gender": "Female",
            "height_cm": 165.0,
            "weight_kg": 68.0,
            "smoking_status": "Never",
            "alcohol_intake": "None",
            "tobacco_use": "No",
            "physical_activity": "Moderate",
            "diet_quality": "Good",
            "sleep_hours": 7,
            "stress_level": "Low",
            "family_history": "No",
            "family_relative": "None",
            "family_cancer_type": "None",
            "has_diabetes": "No",
            "has_hypertension": "No",
            "is_obese": "No",
            "previous_radiation": "No",
            "previous_benign_tumors": "No",
            "pollution_exposure": "Low",
            "chemical_exposure": "Low",
            "uv_exposure": "Low",
            "occupation_risk": "Low",
        }
        response = self.client.post(reverse("risk_assessment"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "AI Risk Report")

