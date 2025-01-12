# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employees/<int:pk>/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('employee-list/', EmployeeList.as_view(), name='employee-list'),
    path('roles/', RoleListView.as_view(), name='role-list'),
]