from django.urls import path
from .views import *

urlpatterns = [
    path('patient-report/', ReportPatient.as_view(), name='patient-report'),
    path('medicine-cost-report/', ReportMedicineCost.as_view(), name='medicine-cost-report'),
]

