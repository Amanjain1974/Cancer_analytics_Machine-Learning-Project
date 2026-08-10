from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):
    """
    Stores every prediction made by a user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    patient_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    race_ethnicity = models.CharField(max_length=50)

    bmi = models.FloatField()

    smoking_status = models.CharField(max_length=30)
    family_history = models.CharField(max_length=10)

    cancer_type = models.CharField(max_length=100)
    stage = models.CharField(max_length=20)
    tumor_size = models.FloatField()

    treatment_type = models.CharField(max_length=100)
    treatment_response = models.CharField(max_length=100)

    survival_months = models.PositiveIntegerField()

    genetic_marker = models.CharField(
        max_length=100,
        default="Unknown"
    )

    hospital_region = models.CharField(max_length=100)

    prediction = models.CharField(max_length=20)
    probability = models.FloatField()
    confidence = models.FloatField()

    recommendation = models.TextField(blank=True)

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
            f"{self.prediction} "
            f"({self.created_at:%d-%m-%Y})"
        )


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

