import json
from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):
    """
    Stores pre-diagnosis AI Cancer Risk Assessments and predictions.
    Retains legacy fields with default values to guarantee zero breaking changes.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    patient_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=40)
    gender = models.CharField(max_length=20, default="Female")
    height_cm = models.FloatField(default=170.0)
    weight_kg = models.FloatField(default=70.0)
    bmi = models.FloatField(default=22.5)

    # Family History
    family_history = models.CharField(max_length=10, default="No")
    family_cancer_type = models.CharField(max_length=100, blank=True, default="None")
    family_affected_count = models.IntegerField(default=0)

    # Lifestyle Factors
    smoking_status = models.CharField(max_length=30, default="Never")
    cigarettes_per_day = models.IntegerField(default=0)
    alcohol_intake = models.CharField(max_length=30, default="Never")
    tobacco_chewing = models.CharField(max_length=10, default="No")
    exercise_frequency = models.CharField(max_length=30, default="1-2 times/week")
    daily_walking_mins = models.IntegerField(default=30)
    sleep_hours = models.IntegerField(default=7)
    stress_level = models.CharField(max_length=30, default="Moderate")
    water_intake_liters = models.FloatField(default=2.0)

    # Dietary Factors
    vegetables_intake = models.CharField(max_length=30, default="Moderate")
    fruits_intake = models.CharField(max_length=30, default="Moderate")
    fast_food_frequency = models.CharField(max_length=30, default="Weekly")
    processed_meat = models.CharField(max_length=10, default="No")
    red_meat = models.CharField(max_length=30, default="Weekly")
    sugary_drinks = models.CharField(max_length=30, default="Weekly")
    junk_food_frequency = models.CharField(max_length=30, default="Moderate")

    # Medical History Conditions
    diabetes = models.CharField(max_length=10, default="No")
    hypertension = models.CharField(max_length=10, default="No")
    obesity = models.CharField(max_length=10, default="No")
    chronic_inflammation = models.CharField(max_length=10, default="No")
    previous_tumors = models.CharField(max_length=10, default="No")
    genetic_disorders = models.CharField(max_length=10, default="No")

    # Symptoms JSON
    symptoms_json = models.TextField(blank=True, default="[]")

    # Environmental & Occupational Factors
    air_pollution = models.CharField(max_length=30, default="Low")
    radiation_exposure = models.CharField(max_length=30, default="Low")
    chemical_exposure = models.CharField(max_length=30, default="Low")
    asbestos_exposure = models.CharField(max_length=30, default="Low")
    occupation_risk = models.CharField(max_length=30, default="Low")
    uv_exposure = models.CharField(max_length=30, default="Low")

    # AI Prediction Metrics
    prediction = models.CharField(max_length=20, default="Low")  # 'Low', 'Medium', 'High'
    probability = models.FloatField(default=0.0)  # 0.0 to 1.0 (or 0 - 100%)
    confidence = models.FloatField(default=90.0)
    health_score = models.IntegerField(default=75)
    future_risk = models.TextField(blank=True, default="")
    risk_reduction_estimate = models.FloatField(default=0.0)
    top_risk_factors_json = models.TextField(blank=True, default="[]")
    recommendations_json = models.TextField(blank=True, default="[]")

    # Legacy fields preserved for 100% database backwards compatibility
    race_ethnicity = models.CharField(max_length=50, blank=True, default="Not Specified")
    cancer_type = models.CharField(max_length=100, blank=True, default="General Risk")
    stage = models.CharField(max_length=20, blank=True, default="Pre-diagnosis")
    tumor_size = models.FloatField(default=0.0)
    treatment_type = models.CharField(max_length=100, blank=True, default="N/A")
    treatment_response = models.CharField(max_length=100, blank=True, default="N/A")
    survival_months = models.PositiveIntegerField(default=0)
    genetic_marker = models.CharField(max_length=100, blank=True, default="Unknown")
    hospital_region = models.CharField(max_length=100, blank=True, default="General")
    recommendation = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["prediction"]),
            models.Index(fields=["cancer_type"]),
        ]

    def __str__(self):
        return (
            f"{self.patient_name} - "
            f"{self.prediction} Risk ({self.probability * 100 if self.probability <= 1 else self.probability:.1f}%) "
            f"({self.created_at:%d-%m-%Y})"
        )

    def get_top_factors(self):
        try:
            return json.loads(self.top_risk_factors_json)
        except Exception:
            return []

    def get_recommendations(self):
        try:
            return json.loads(self.recommendations_json)
        except Exception:
            return [self.recommendation] if self.recommendation else []

    def get_symptoms(self):
        try:
            return json.loads(self.symptoms_json)
        except Exception:
            return []


class RiskAssessmentHistory(models.Model):
    """
    Stores pre-diagnosis cancer risk assessments for healthy individuals.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="risk_assessments"
    )

    patient_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    height_cm = models.FloatField(default=170.0)
    weight_kg = models.FloatField(default=70.0)
    bmi = models.FloatField()

    # Lifestyle Factors
    smoking_status = models.CharField(max_length=30)
    alcohol_intake = models.CharField(max_length=30)
    tobacco_use = models.CharField(max_length=10)
    physical_activity = models.CharField(max_length=30)
    diet_quality = models.CharField(max_length=30)
    sleep_hours = models.PositiveIntegerField(default=7)
    stress_level = models.CharField(max_length=30)

    # Family History
    family_history = models.CharField(max_length=10)
    family_relative = models.CharField(max_length=50, blank=True, default="None")
    family_cancer_type = models.CharField(max_length=100, blank=True, default="None")

    # Medical History
    has_diabetes = models.CharField(max_length=10)
    has_hypertension = models.CharField(max_length=10)
    is_obese = models.CharField(max_length=10)
    previous_radiation = models.CharField(max_length=10)
    previous_benign_tumors = models.CharField(max_length=10)

    # Environmental & Occupational Factors
    pollution_exposure = models.CharField(max_length=30)
    chemical_exposure = models.CharField(max_length=30)
    uv_exposure = models.CharField(max_length=30)
    occupation_risk = models.CharField(max_length=30)

    # Assessment Results
    overall_risk = models.CharField(max_length=20)  # Low, Medium, High
    risk_percentage = models.FloatField()
    confidence = models.FloatField()
    top_risk_factors = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["overall_risk"]),
        ]

    def __str__(self):
        return (
            f"{self.patient_name} - "
            f"{self.overall_risk} Risk ({self.risk_percentage:.1f}%) - "
            f"({self.created_at:%d-%m-%Y})"
        )
