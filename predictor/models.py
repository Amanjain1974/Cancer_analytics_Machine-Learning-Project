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
