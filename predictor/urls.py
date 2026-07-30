from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("predict/", views.predict_cancer, name="predict"),
    path("history/", views.history, name="history"),
    path("analytics/", views.analytics, name="analytics"),
]
