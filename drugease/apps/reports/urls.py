from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('patients/', views.ReportPatient, name='gender_age_distribution'),
    path('medicines/', views.report_medicine_cost, name='report_medicine_cost'),
]
