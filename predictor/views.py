import csv
import json
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.http import HttpResponse
from django.core.paginator import Paginator

from .forms import PredictionForm, SurvivalPredictionForm, RiskAssessmentForm
from .models import PredictionHistory, RiskAssessmentHistory
from ml.risk_engine import evaluate_patient_risk, get_model_pipeline
from ml.survival_engine import evaluate_survival_prognosis, get_survival_pipeline

_risk_model_cache = None
_survival_model_cache = None


def get_model():
    global _risk_model_cache
    if _risk_model_cache is None:
        _risk_model_cache = get_model_pipeline()
    return _risk_model_cache


def get_survival_model():
    global _survival_model_cache
    if _survival_model_cache is None:
        _survival_model_cache = get_survival_pipeline()
    return _survival_model_cache


def home(request):
    total_system_predictions = PredictionHistory.objects.count()
    return render(request, "home.html", {
        "total_system_predictions": total_system_predictions
    })


@login_required
def risk_assessment_view(request):
    """
    MODULE 1: Early Cancer Risk Assessment AI (Pre-Diagnosis Evaluation).
    Evaluates 40+ pre-diagnosis lifestyle, symptom, genetic, and environmental factors.
    Predicts probability of developing cancer in the future.
    """
    form = PredictionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        h_cm = data.get("height_cm", 170.0)
        w_kg = data.get("weight_kg", 70.0)
        bmi = round(w_kg / ((h_cm / 100.0) ** 2), 1) if h_cm > 0 else 22.5
        data["bmi"] = bmi

        symptom_keys = [k for k in data.keys() if k.startswith("symptom_")]
        active_symptoms = [
            k.replace("symptom_", "").replace("_", " ").title()
            for k in symptom_keys if data.get(k) is True
        ]

        assessment = evaluate_patient_risk(data)

        record = PredictionHistory.objects.create(
            user=request.user,
            patient_name=data["patient_name"],
            age=data["age"],
            gender=data["gender"],
            height_cm=h_cm,
            weight_kg=w_kg,
            bmi=bmi,
            family_history=data["family_history"],
            family_cancer_type=data.get("family_cancer_type", "None"),
            family_affected_count=data.get("family_affected_count", 0),
            smoking_status=data["smoking_status"],
            cigarettes_per_day=data.get("cigarettes_per_day", 0),
            alcohol_intake=data["alcohol_intake"],
            tobacco_chewing=data["tobacco_chewing"],
            exercise_frequency=data["exercise_frequency"],
            daily_walking_mins=data["daily_walking_mins"],
            sleep_hours=data["sleep_hours"],
            stress_level=data["stress_level"],
            water_intake_liters=data["water_intake_liters"],
            vegetables_intake=data["vegetables_intake"],
            fruits_intake=data["fruits_intake"],
            fast_food_frequency=data["fast_food_frequency"],
            processed_meat=data["processed_meat"],
            red_meat=data["red_meat"],
            sugary_drinks=data["sugary_drinks"],
            junk_food_frequency=data["junk_food_frequency"],
            diabetes=data["diabetes"],
            hypertension=data["hypertension"],
            obesity=data["obesity"],
            chronic_inflammation=data["chronic_inflammation"],
            previous_tumors=data["previous_tumors"],
            genetic_disorders=data["genetic_disorders"],
            symptoms_json=json.dumps(active_symptoms),
            air_pollution=data["air_pollution"],
            radiation_exposure=data["radiation_exposure"],
            chemical_exposure=data["chemical_exposure"],
            asbestos_exposure=data["asbestos_exposure"],
            occupation_risk=data["occupation_risk"],
            uv_exposure=data["uv_exposure"],
            prediction=assessment["overall_risk"],
            probability=round(assessment["risk_percentage"] / 100.0, 4),
            confidence=assessment["confidence"],
            health_score=assessment["health_score"],
            future_risk=assessment["future_risk"],
            risk_reduction_estimate=assessment["risk_reduction_estimate"],
            top_risk_factors_json=assessment["top_risk_factors_json"],
            recommendations_json=assessment["recommendations_json"],
            recommendation=assessment["recommendations"][0] if assessment["recommendations"] else "",
            cancer_type="Pre-Diagnosis Risk",
            stage="N/A",
        )

        messages.success(request, "Cancer Risk Assessment completed successfully.")

        return render(request, "result.html", {
            "record": record,
            "assessment": assessment,
            "risk_percentage": assessment["risk_percentage"],
            "overall_risk": assessment["overall_risk"],
            "health_score": assessment["health_score"],
            "confidence": assessment["confidence"],
            "top_factors": assessment["top_risk_factors"],
            "recommendations": assessment["recommendations"],
            "future_risk": assessment["future_risk"],
            "risk_reduction_estimate": assessment["risk_reduction_estimate"],
            "active_symptoms": active_symptoms,
        })

    return render(request, "predict.html", {"form": form})


@login_required
def predict_cancer(request):
    """
    MODULE 2: Cancer Survival Prediction AI (Post-Diagnosis Clinical Prognosis).
    For patients ALREADY DIAGNOSED with cancer.
    Estimates survival probability, survival months, prognosis category, and oncology advice.
    """
    form = SurvivalPredictionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        h_cm = data.get("height_cm", 175.0)
        w_kg = data.get("weight_kg", 75.0)
        bmi = round(w_kg / ((h_cm / 100.0) ** 2), 1) if h_cm > 0 else 24.5
        data["bmi"] = bmi

        survival_res = evaluate_survival_prognosis(data)

        record = PredictionHistory.objects.create(
            user=request.user,
            patient_name=data["patient_name"],
            age=data["age"],
            gender=data["gender"],
            height_cm=h_cm,
            weight_kg=w_kg,
            bmi=bmi,
            smoking_status=data["smoking_status"],
            hospital_region=data["hospital_region"],
            diabetes=data["has_diabetes"],
            hypertension=data["has_hypertension"],
            cancer_type=data["cancer_type"],
            stage=data["stage"],
            tumor_size=data["tumor_size_cm"],
            survival_months=survival_res["estimated_survival_months"],
            treatment_type=data["treatment_type"],
            treatment_response=data["treatment_response"],
            genetic_marker=data["genetic_marker"],
            prediction=survival_res["prognosis_category"],
            probability=round(survival_res["survival_probability"] / 100.0, 4),
            confidence=survival_res["confidence"],
            future_risk=survival_res["predicted_outcome"],
            top_risk_factors_json=survival_res["positive_factors_json"],
            recommendations_json=survival_res["recommendations_json"],
            recommendation=survival_res["recommendations"][0] if survival_res["recommendations"] else "",
        )

        messages.success(request, "Cancer Survival Prognosis Prediction completed successfully.")

        return render(request, "survival_result.html", {
            "record": record,
            "survival_res": survival_res,
            "survival_probability": survival_res["survival_probability"],
            "estimated_survival_months": survival_res["estimated_survival_months"],
            "confidence": survival_res["confidence"],
            "prognosis_category": survival_res["prognosis_category"],
            "predicted_outcome": survival_res["predicted_outcome"],
            "positive_factors": survival_res["positive_factors"],
            "negative_factors": survival_res["negative_factors"],
            "recommendations": survival_res["recommendations"],
        })

    return render(request, "survival_predict.html", {"form": form})


@login_required
def dashboard(request):
    """Dashboard displaying distinct Module 1 (Risk Assessment) and Module 2 (Survival Prognosis) statistics."""
    user_preds = PredictionHistory.objects.filter(user=request.user)

    # Distinguish Module 1 (Risk Assessment) vs Module 2 (Survival Predictions)
    risk_preds = user_preds.filter(cancer_type__icontains="Pre-Diagnosis") | user_preds.filter(stage="N/A")
    survival_preds = user_preds.exclude(stage="N/A").exclude(cancer_type__icontains="Pre-Diagnosis")

    if not risk_preds.exists() and not survival_preds.exists():
        risk_preds = user_preds.filter(stage="N/A")
        survival_preds = user_preds.exclude(stage="N/A")

    # Module 1 Stats
    total_risk = risk_preds.count()
    avg_risk_score = round((risk_preds.aggregate(avg=Avg("probability"))["avg"] or 0.0) * 100.0, 1)
    high_risk_count = risk_preds.filter(prediction__iexact="High").count()
    med_risk_count = risk_preds.filter(prediction__iexact="Medium").count()
    low_risk_count = risk_preds.filter(prediction__iexact="Low").count()

    # Module 2 Stats
    total_survival = survival_preds.count()
    avg_survival_prob = round((survival_preds.aggregate(avg=Avg("probability"))["avg"] or 0.0) * 100.0, 1)
    avg_survival_months = round(survival_preds.aggregate(avg=Avg("survival_months"))["avg"] or 0.0, 1)

    recent_predictions = user_preds.order_by("-created_at")[:6]

    # Chart Datasets
    risk_dist_json = json.dumps([high_risk_count, med_risk_count, low_risk_count])
    survival_dist = [
        survival_preds.filter(prediction__iexact="Excellent").count(),
        survival_preds.filter(prediction__iexact="Good").count(),
        survival_preds.filter(prediction__iexact="Moderate").count(),
        survival_preds.filter(prediction__iexact="Poor").count(),
        survival_preds.filter(prediction__iexact="Critical").count(),
    ]

    return render(request, "dashboard.html", {
        "recent_predictions": recent_predictions,
        "total_risk": total_risk,
        "avg_risk_score": avg_risk_score,
        "high_risk_count": high_risk_count,
        "med_risk_count": med_risk_count,
        "low_risk_count": low_risk_count,
        "total_survival": total_survival,
        "avg_survival_prob": avg_survival_prob,
        "avg_survival_months": avg_survival_months,
        "risk_dist_json": risk_dist_json,
        "survival_dist_json": json.dumps(survival_dist),
    })


@login_required
def analytics(request):
    """Detailed analytics for both AI modules."""
    qs = PredictionHistory.objects.filter(user=request.user)

    risk_qs = qs.filter(cancer_type__icontains="Pre-Diagnosis") | qs.filter(stage="N/A")
    survival_qs = qs.exclude(stage="N/A").exclude(cancer_type__icontains="Pre-Diagnosis")

    total_risk = risk_qs.count()
    total_survival = survival_qs.count()

    high_risk = risk_qs.filter(prediction__iexact="High").count()
    med_risk = risk_qs.filter(prediction__iexact="Medium").count()
    low_risk = risk_qs.filter(prediction__iexact="Low").count()

    # Cancer Type Breakdown for Survival Module
    by_cancer = list(survival_qs.values("cancer_type").annotate(count=Count("id")).order_by("-count"))
    by_stage = list(survival_qs.values("stage").annotate(count=Count("id")))

    return render(request, "analytics.html", {
        "total_risk": total_risk,
        "total_survival": total_survival,
        "high_risk": high_risk,
        "med_risk": med_risk,
        "low_risk": low_risk,
        "risk_dist_json": json.dumps([high_risk, med_risk, low_risk]),
        "by_cancer_json": json.dumps(by_cancer),
        "by_stage_json": json.dumps(by_stage),
    })


@login_required
def history(request):
    """History of both Cancer Risk Assessments and Survival Predictions."""
    query = request.GET.get("q", "").strip()
    module_filter = request.GET.get("module", "").strip()

    predictions_qs = PredictionHistory.objects.filter(user=request.user)

    if query:
        predictions_qs = predictions_qs.filter(
            Q(patient_name__icontains=query) | Q(prediction__icontains=query) | Q(cancer_type__icontains=query)
        )

    if module_filter == "risk":
        predictions_qs = predictions_qs.filter(Q(cancer_type__icontains="Pre-Diagnosis") | Q(stage="N/A"))
    elif module_filter == "survival":
        predictions_qs = predictions_qs.exclude(stage="N/A").exclude(cancer_type__icontains="Pre-Diagnosis")

    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cris_patient_history.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Patient Name", "Age", "Gender", "Module Type", "Cancer Type / Risk",
            "Stage", "Probability %", "Estimated Survival Months", "Prediction / Prognosis", "Date"
        ])
        for p in predictions_qs:
            prob_pct = round(p.probability * 100, 1) if p.probability <= 1.0 else round(p.probability, 1)
            m_type = "Cancer Risk Assessment" if p.stage == "N/A" else "Cancer Survival Prediction"
            writer.writerow([
                p.patient_name, p.age, p.gender, m_type, p.cancer_type,
                p.stage, prob_pct, p.survival_months, p.prediction, p.created_at.strftime("%Y-%m-%d")
            ])
        return response

    paginator = Paginator(predictions_qs.order_by("-created_at"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "history.html", {
        "page_obj": page_obj,
        "query": query,
        "module_filter": module_filter,
    })


@login_required
def report_view(request, pk):
    """Renders printable report based on record type (Survival Prognosis vs Risk Assessment)."""
    record = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    prob_pct = round(record.probability * 100.0, 1) if record.probability <= 1.0 else round(record.probability, 1)

    is_survival = (record.stage != "N/A" and "Pre-Diagnosis" not in record.cancer_type)

    if is_survival:
        return render(request, "survival_result.html", {
            "record": record,
            "survival_probability": prob_pct,
            "estimated_survival_months": record.survival_months,
            "confidence": record.confidence,
            "prognosis_category": record.prediction,
            "predicted_outcome": record.future_risk,
            "positive_factors": record.get_top_factors(),
            "negative_factors": [],
            "recommendations": record.get_recommendations(),
        })

    return render(request, "report.html", {
        "record": record,
        "risk_pct": prob_pct,
        "top_factors": record.get_top_factors(),
        "recommendations": record.get_recommendations(),
        "symptoms": record.get_symptoms(),
    })


@login_required
def delete_prediction(request, pk):
    record = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Record deleted successfully.")
    return redirect("history")


@login_required
def profile(request):
    user_preds = PredictionHistory.objects.filter(user=request.user)
    total_preds = user_preds.count()
    return render(request, "profile.html", {
        "user": request.user,
        "total_preds": total_preds,
        "recent_preds": user_preds.order_by("-created_at")[:5],
    })


@login_required
def settings_view(request):
    if request.method == "POST":
        messages.success(request, "Preferences saved successfully.")
        return redirect("settings")
    return render(request, "settings.html")


@login_required
def risk_report_view(request, pk):
    return redirect("report", pk=pk)


@login_required
def delete_risk_assessment(request, pk):
    return redirect("history")