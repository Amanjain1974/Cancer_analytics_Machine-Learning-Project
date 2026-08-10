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

    def test_authenticated_risk_assessment_view_get(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        response = self.client.get(reverse("risk_assessment"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancer Risk Assessment AI")

    def test_authenticated_survival_prediction_view_get(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        response = self.client.get(reverse("predict"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cancer Survival Prediction AI")

    def test_risk_assessment_form_submission(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        payload = {
            "patient_name": "Jane Doe",
            "age": 45,
            "gender": "Female",
            "height_cm": 165.0,
            "weight_kg": 68.0,
            "family_history": "Yes",
            "family_cancer_type": "Breast",
            "family_affected_count": 2,
            "smoking_status": "Daily",
            "cigarettes_per_day": 20,
            "alcohol_intake": "Weekly",
            "tobacco_chewing": "No",
            "exercise_frequency": "Sedentary",
            "daily_walking_mins": 15,
            "sleep_hours": 6,
            "stress_level": "High",
            "water_intake_liters": 1.5,
            "vegetables_intake": "Low",
            "fruits_intake": "Low",
            "fast_food_frequency": "Daily",
            "processed_meat": "Yes",
            "red_meat": "Daily",
            "sugary_drinks": "Daily",
            "junk_food_frequency": "High",
            "diabetes": "No",
            "hypertension": "Yes",
            "obesity": "No",
            "chronic_inflammation": "Yes",
            "previous_tumors": "No",
            "genetic_disorders": "No",
            "symptom_cough": True,
            "symptom_weight_loss": True,
            "air_pollution": "Moderate",
            "radiation_exposure": "High",
            "chemical_exposure": "Moderate",
            "asbestos_exposure": "Low",
            "occupation_risk": "Moderate",
            "uv_exposure": "Moderate",
        }
        response = self.client.post(reverse("risk_assessment"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "Risk Assessment for")
        self.assertTrue(PredictionHistory.objects.filter(patient_name="Jane Doe").exists())

    def test_survival_prediction_form_submission(self):
        self.client.login(username="testdoctor", password="TestPassword123!")
        payload = {
            "patient_name": "John Smith",
            "age": 55,
            "gender": "Male",
            "height_cm": 178.0,
            "weight_kg": 80.0,
            "smoking_status": "Former",
            "hospital_region": "North",
            "has_diabetes": "No",
            "has_hypertension": "Yes",
            "has_heart_disease": "No",
            "has_kidney_disease": "No",
            "cancer_type": "Colon",
            "stage": "Stage II",
            "tumor_size_cm": 3.2,
            "diagnosis_months": 8,
            "metastasis": "No",
            "lymph_nodes": "No",
            "genetic_marker": "KRAS",
            "treatment_type": "Surgery",
            "treatment_response": "Excellent",
        }
        response = self.client.post(reverse("predict"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Smith")
        self.assertContains(response, "Clinical Survival Report for")
        self.assertTrue(PredictionHistory.objects.filter(patient_name="John Smith", cancer_type="Colon").exists())
