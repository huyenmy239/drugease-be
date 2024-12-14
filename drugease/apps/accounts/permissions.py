# accounts/permissions.py
from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'doctor'

class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'pharmacist'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'staff'