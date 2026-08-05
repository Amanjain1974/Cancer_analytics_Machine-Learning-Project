from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("predict/", views.predict_cancer, name="predict"),
    path("history/", views.history, name="history"),
    path("analytics/", views.analytics, name="analytics"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings_view, name="settings"),
    path("report/<int:pk>/", views.report_view, name="report"),
    path("delete-prediction/<int:pk>/", views.delete_prediction, name="delete_prediction"),
]
