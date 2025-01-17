from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"patients", PatientViewSet)
router.register(r"prescriptions", PrescriptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "prescription-list/", PrescriptionListView.as_view(), name="prescription-list"
    ),
    path("patient-list/", PatientListView.as_view(), name="patient-list"),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("medicines/", MedicineListView.as_view(), name="medicine-list"),
]
