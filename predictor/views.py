import pandas as pd

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PredictionForm
from .models import PredictionHistory
from .utils import load_model

_model = None


def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    recent_predictions = PredictionHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    return render(request, "dashboard.html", {
        "recent_predictions": recent_predictions,
        "total_predictions": PredictionHistory.objects.filter(
            user=request.user
        ).count(),
    })


@login_required
def predict_cancer(request):
    form = PredictionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        data = form.cleaned_data
        model = get_model()

        # Create DataFrame with EXACT column names used during training
        features = pd.DataFrame([{
            "Age": data["age"],
            "Gender": data["gender"],
            "Race/Ethnicity": data["race_ethnicity"],
            "BMI": data["bmi"],
            "SmokingStatus": data["smoking_status"],
            "FamilyHistory": data["family_history"],
            "CancerType": data["cancer_type"],
            "Stage": data["stage"],
            "TumorSize": data["tumor_size"],
            "TreatmentType": data["treatment_type"],
            "TreatmentResponse": data["treatment_response"],
            "SurvivalMonths": data["survival_months"],
            "GeneticMarker": data["genetic_marker"] or "Unknown",
            "HospitalRegion": data["hospital_region"],
        }])

        prediction = model.predict(features)[0]

        probability = 0.0
        confidence = 0.0

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(features)[0]
            probability = float(max(probs))
            confidence = probability * 100

        PredictionHistory.objects.create(
            user=request.user,
            **data,
            prediction=str(prediction),
            probability=probability,
            confidence=confidence,
            recommendation=(
                "Consult an oncologist immediately."
                if str(prediction).lower() == "yes"
                else "Continue routine follow-up."
            ),
        )

        messages.success(request, "Prediction completed successfully.")

        return render(request, "result.html", {
            "prediction": prediction,
            "probability": probability,
            "confidence": confidence,
        })

    return render(request, "predict.html", {"form": form})


@login_required
def history(request):
    predictions = PredictionHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "history.html", {
        "predictions": predictions
    })


@login_required
def analytics(request):
    qs = PredictionHistory.objects.filter(user=request.user)

    return render(request, "analytics.html", {
        "total": qs.count(),
        "positive": qs.filter(prediction="Yes").count(),
        "negative": qs.filter(prediction="No").count(),
        "history": qs[:10],
    })