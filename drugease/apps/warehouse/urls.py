from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"medicines", MedicineViewSet)
router.register(r"warehouses", WarehouseViewSet)
router.register(r"import-receipts", ImportReceiptViewSet)
router.register(r"import-receipt-details", ImportReceiptDetailViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("medicines/", MedicineListView.as_view(), name="medicine-list"),
    path("warehouses/", WarehouseListAPIView.as_view(), name="warehouse-list"),
    path(
        "import-receipts/",
        ImportReceiptListAPIView.as_view(),
        name="import-receipts-list",
    ),
    path(
        "import-receipt-details/<int:pk>/",
        ImportReceiptDetailAPIView.as_view(),
        name="import-receipt-details-list",
    ),
]
