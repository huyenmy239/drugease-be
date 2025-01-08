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
    path("medicine-list/", MedicineListView.as_view(), name="medicine-list"),
    path("warehouse-list/", WarehouseListAPIView.as_view(), name="warehouse-list"),
    path(
        "warehouse-list/<int:pk>/",
        WarehouseDetailAPIView.as_view(),
        name="warehouse-detail",
    ),
    path(
        "import-receipt-list/",
        ImportReceiptListAPIView.as_view(),
        name="import-receipts-list",
    ),
    path(
        "import-receipt-list/<int:pk>/",
        ImportReceiptAPIView.as_view(),
        name="ir-list-id",
    ),
    path(
        "import-receipt-detail-list/",
        ImportReceiptDetailListAPIView.as_view(),
        name="ir-detail-list-id",
    ),
    path(
        "import-receipt-detail-list/<int:pk>/",
        ImportReceiptDetailAPIView.as_view(),
        name="ir-detail-list-id",
    ),
]
