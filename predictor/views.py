import json
import pandas as pd

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg

from .forms import PredictionForm, RiskAssessmentForm
from .models import PredictionHistory, RiskAssessmentHistory
from .utils import load_model
from ml.risk_engine import get_risk_assessment

_model = None


def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model


def home(request):
    total_system_predictions = PredictionHistory.objects.count()
    return render(request, "home.html", {
        "total_system_predictions": total_system_predictions
    })


@login_required
def dashboard(request):
    # Survival Predictions Stats (Module 2)
    user_preds = PredictionHistory.objects.filter(user=request.user)
    recent_predictions = user_preds.order_by("-created_at")[:5]
    total_predictions = user_preds.count()
    positive_count = user_preds.filter(prediction__iexact="yes").count()
    negative_count = user_preds.filter(prediction__iexact="no").count()

    # Risk Assessments Stats (Module 1)
    user_risk = RiskAssessmentHistory.objects.filter(user=request.user)
    recent_risk_assessments = user_risk.order_by("-created_at")[:5]
    total_risk_assessments = user_risk.count()
    high_risk_count = user_risk.filter(overall_risk__iexact="High").count()
    med_risk_count = user_risk.filter(overall_risk__iexact="Medium").count()
    low_risk_count = user_risk.filter(overall_risk__iexact="Low").count()

    # Aggregated System Averages
    avg_conf_qs = user_preds.aggregate(avg=Avg("confidence"))
    avg_confidence = round(avg_conf_qs["avg"], 1) if avg_conf_qs["avg"] else 0.0

    avg_risk_pct_qs = user_risk.aggregate(avg=Avg("risk_percentage"))
    avg_risk_pct = round(avg_risk_pct_qs["avg"], 1) if avg_risk_pct_qs["avg"] else 0.0

    # Chart data: Cancer types breakdown
    cancer_types = list(user_preds.values("cancer_type").annotate(count=Count("id")))

    # Recent predictions trend
    trend_qs = list(user_preds.order_by("-created_at")[:10])
    trend_qs.reverse()
    trend_labels = [p.created_at.strftime("%b %d") for p in trend_qs]
    trend_scores = [round(p.confidence, 1) for p in trend_qs]

    # Risk Assessment Distribution Chart
    risk_dist_json = json.dumps([high_risk_count, med_risk_count, low_risk_count])

    return render(request, "dashboard.html", {
        "recent_predictions": recent_predictions,
        "total_predictions": total_predictions,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "avg_confidence": avg_confidence,
        "recent_risk_assessments": recent_risk_assessments,
        "total_risk_assessments": total_risk_assessments,
        "high_risk_count": high_risk_count,
        "med_risk_count": med_risk_count,
        "low_risk_count": low_risk_count,
        "avg_risk_pct": avg_risk_pct,
        "cancer_types_json": json.dumps(cancer_types),
        "trend_labels_json": json.dumps(trend_labels),
        "trend_scores_json": json.dumps(trend_scores),
        "risk_dist_json": risk_dist_json,
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
            confidence = round(probability * 100, 2)

        recommendation = (
            "Consult an oncologist immediately. High risk indicators detected. Follow up with comprehensive diagnostic imaging and biopsy confirmation."
            if str(prediction).lower() == "yes"
            else "Continue routine screening and maintain healthy lifestyle habits. Low immediate risk detected."
        )

        record = PredictionHistory.objects.create(
            user=request.user,
            **data,
            prediction=str(prediction),
            probability=round(probability, 4),
            confidence=confidence,
            recommendation=recommendation,
        )

        messages.success(request, "Prediction completed successfully.")

        return render(request, "result.html", {
            "prediction": prediction,
            "probability": round(probability, 4),
            "confidence": confidence,
            "record": record,
            "recommendation": recommendation,
        })

    return render(request, "predict.html", {"form": form})


@login_required
def history(request):
    predictions = PredictionHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    risk_assessments = RiskAssessmentHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "history.html", {
        "predictions": predictions,
        "risk_assessments": risk_assessments,
    })


@login_required
def analytics(request):
    # Survival Module Stats (Module 2)
    qs = PredictionHistory.objects.filter(user=request.user)
    total = qs.count()
    positive = qs.filter(prediction__iexact="yes").count()
    negative = qs.filter(prediction__iexact="no").count()

    avg_conf_qs = qs.aggregate(avg=Avg("confidence"))
    avg_confidence = round(avg_conf_qs["avg"], 1) if avg_conf_qs["avg"] else 0.0

    by_cancer = list(qs.values("cancer_type").annotate(count=Count("id")).order_by("-count"))
    by_region = list(qs.values("hospital_region").annotate(count=Count("id")))

    high_conf = qs.filter(confidence__gte=85).count()
    med_conf = qs.filter(confidence__gte=70, confidence__lt=85).count()
    low_conf = qs.filter(confidence__lt=70).count()

    # Risk Assessment Stats (Module 1)
    risk_qs = RiskAssessmentHistory.objects.filter(user=request.user)
    total_risk_assessments = risk_qs.count()
    high_risk_count = risk_qs.filter(overall_risk__iexact="High").count()
    med_risk_count = risk_qs.filter(overall_risk__iexact="Medium").count()
    low_risk_count = risk_qs.filter(overall_risk__iexact="Low").count()

    smoking_dist = list(risk_qs.values("smoking_status").annotate(count=Count("id")))
    family_dist = list(risk_qs.values("family_history").annotate(count=Count("id")))

    return render(request, "analytics.html", {
        "total": total,
        "positive": positive,
        "negative": negative,
        "avg_confidence": avg_confidence,
        "history": qs[:10],
        "by_cancer_json": json.dumps(by_cancer),
        "by_region_json": json.dumps(by_region),
        "conf_dist_json": json.dumps([high_conf, med_conf, low_conf]),
        "total_risk_assessments": total_risk_assessments,
        "high_risk_count": high_risk_count,
        "med_risk_count": med_risk_count,
        "low_risk_count": low_risk_count,
        "risk_strata_json": json.dumps([high_risk_count, med_risk_count, low_risk_count]),
        "smoking_dist_json": json.dumps(smoking_dist),
        "family_dist_json": json.dumps(family_dist),
    })


@login_required
def profile(request):
    user_preds = PredictionHistory.objects.filter(user=request.user)
    total_preds = user_preds.count()
    pos_preds = user_preds.filter(prediction__iexact="yes").count()
    neg_preds = user_preds.filter(prediction__iexact="no").count()

    return render(request, "profile.html", {
        "user": request.user,
        "total_preds": total_preds,
        "pos_preds": pos_preds,
        "neg_preds": neg_preds,
        "recent_preds": user_preds.order_by("-created_at")[:5],
    })


@login_required
def settings_view(request):
    if request.method == "POST":
        messages.success(request, "Preferences saved successfully.")
        return redirect("settings")
    return render(request, "settings.html")


@login_required
def report_view(request, pk):
    record = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    return render(request, "report.html", {
        "record": record,
        "prediction": record.prediction,
        "probability": record.probability,
        "confidence": record.confidence,
        "recommendation": record.recommendation,
    })


@login_required
def delete_prediction(request, pk):
    record = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Prediction record deleted successfully.")
        return redirect("history")
    return redirect("history")


@login_required
def risk_assessment_view(request):
    form = RiskAssessmentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        # Calculate BMI automatically from height & weight
        h_cm = data["height_cm"]
        w_kg = data["weight_kg"]
        bmi = round(w_kg / ((h_cm / 100) ** 2), 1) if h_cm > 0 else 22.0

        # Execute Modular Clinical Risk Engine
        assessment = get_risk_assessment(data)

        # Save assessment record to RiskAssessmentHistory
        top_factors_str = "\n".join(assessment["top_risk_factors"])
        recs_str = "\n".join(assessment["recommendations"])

        record = RiskAssessmentHistory.objects.create(
            user=request.user,
            patient_name=data["patient_name"],
            age=data["age"],
            gender=data["gender"],
            height_cm=h_cm,
            weight_kg=w_kg,
            bmi=bmi,
            smoking_status=data["smoking_status"],
            alcohol_intake=data["alcohol_intake"],
            tobacco_use=data["tobacco_use"],
            physical_activity=data["physical_activity"],
            diet_quality=data["diet_quality"],
            sleep_hours=data["sleep_hours"],
            stress_level=data["stress_level"],
            family_history=data["family_history"],
            family_relative=data.get("family_relative") or "None",
            family_cancer_type=data.get("family_cancer_type") or "None",
            has_diabetes=data["has_diabetes"],
            has_hypertension=data["has_hypertension"],
            is_obese=data["is_obese"],
            previous_radiation=data["previous_radiation"],
            previous_benign_tumors=data["previous_benign_tumors"],
            pollution_exposure=data["pollution_exposure"],
            chemical_exposure=data["chemical_exposure"],
            uv_exposure=data["uv_exposure"],
            occupation_risk=data["occupation_risk"],
            overall_risk=assessment["overall_risk"],
            risk_percentage=assessment["risk_percentage"],
            confidence=assessment["confidence"],
            top_risk_factors=top_factors_str,
            recommendations=recs_str,
        )

        messages.success(request, "Cancer Risk Assessment completed successfully.")

        return render(request, "risk_report.html", {
            "record": record,
            "top_factors_list": assessment["top_risk_factors"],
            "recommendations_list": assessment["recommendations"],
        })

    return render(request, "risk_assessment.html", {"form": form})


@login_required
def risk_report_view(request, pk):
    record = get_object_or_404(RiskAssessmentHistory, pk=pk, user=request.user)
    top_factors_list = [f.strip() for f in record.top_risk_factors.split("\n") if f.strip()]
    recommendations_list = [r.strip() for r in record.recommendations.split("\n") if r.strip()]

    return render(request, "risk_report.html", {
        "record": record,
        "top_factors_list": top_factors_list,
        "recommendations_list": recommendations_list,
    })


@login_required
def delete_risk_assessment(request, pk):
    record = get_object_or_404(RiskAssessmentHistory, pk=pk, user=request.user)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Risk assessment record deleted successfully.")
        return redirect("history")
    return redirect("history")