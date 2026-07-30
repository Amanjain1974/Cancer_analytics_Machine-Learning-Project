from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PredictionForm
from .models import PredictionHistory
from .utils import load_model

_model=None

def get_model():
    global _model
    if _model is None:
        _model=load_model()
    return _model

def home(request):
    return render(request,"predictor/home.html")

@login_required
def dashboard(request):
    recent_predictions=PredictionHistory.objects.filter(user=request.user).order_by("-created_at")[:5]
    return render(request,"predictor/dashboard.html",{
        "recent_predictions":recent_predictions,
        "total_predictions":PredictionHistory.objects.filter(user=request.user).count(),
    })

@login_required
def predict_cancer(request):
    form=PredictionForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        data=form.cleaned_data
        model=get_model()
        features=[[
            data["age"],data["gender"],data["race_ethnicity"],data["bmi"],
            data["smoking_status"],data["family_history"],data["cancer_type"],
            data["stage"],data["tumor_size"],data["treatment_type"],
            data["treatment_response"],data["survival_months"],
            data["genetic_marker"] or "Unknown",data["hospital_region"]
        ]]
        pred=model.predict(features)[0]
        prob=0.0
        conf=0.0
        if hasattr(model,"predict_proba"):
            p=model.predict_proba(features)[0]
            prob=float(max(p)); conf=prob*100
        PredictionHistory.objects.create(
            user=request.user,**data,prediction=str(pred),
            probability=prob,confidence=conf,
            recommendation="Consult an oncologist immediately." if str(pred).lower()=="yes" else "Continue routine follow-up."
        )
        messages.success(request,"Prediction completed successfully.")
        return render(request,"predictor/result.html",{"prediction":pred,"probability":prob,"confidence":conf})
    return render(request,"predictor/predict.html",{"form":form})

@login_required
def history(request):
    predictions=PredictionHistory.objects.filter(user=request.user).order_by("-created_at")
    return render(request,"predictor/history.html",{"predictions":predictions})

@login_required
def analytics(request):
    qs=PredictionHistory.objects.filter(user=request.user)
    return render(request,"predictor/analytics.html",{
        "total":qs.count(),
        "positive":qs.filter(prediction="Yes").count(),
        "negative":qs.filter(prediction="No").count(),
        "history":qs[:10],
    })
