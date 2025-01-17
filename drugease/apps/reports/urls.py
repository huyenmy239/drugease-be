from django.urls import path
from .views import *

urlpatterns = [
<<<<<<< HEAD
    path('patient-report/', ReportPatient.as_view(), name='patient-report'),
    path('medicine-cost-report/', ReportMedicineCost.as_view(), name='medicine-cost-report'),
]

=======
    path('number-of-prescriptions', NumberofPrescriptionsPrescribedReportAPIView.as_view(), name='number-of-prescriptions'),
    path('med-in-prescription', MedicationsinPrescriptionReportAPIView.as_view(), name='med-in-prescription'),
    path('medicine-export', MedicineExportReportAPIView.as_view(), name='medicine-export'),
    path('doctor', DoctorReportAPIView.as_view(), name='doctor'),
    path('pharmacist', PharmacistReportAPIView.as_view(), name='pharmacist'),
    path('medicine-revenue', MedicineRevenueReportAPIView.as_view(), name='medicine-revenue'),
    path("inventory/", ReportInventory.as_view(), name="report-inventory"),
    path(
        "import-receipt/",
        ReportImportReceipt.as_view(),
        name="report-import-receipt",
    ),
    path(
        "employee-activity/",
        ReportEmployeeActivity.as_view(),
        name="report-employee-activity",
    ),
]
>>>>>>> 221eb584e957ca1f61a11301cdea0185cb16971d
