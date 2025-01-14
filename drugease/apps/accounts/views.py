from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from .models import Account, Employee
from .serializers import *


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # def get_permissions(self):
    #     """
    #     Custom permissions for each action.
    #     """
    #     if self.action in ['register', 'login']:
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Register a new account.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Hash the password
        validated_data = serializer.validated_data
        validated_data['password'] = make_password(validated_data['password'])

        # Save the account
        account = serializer.save()

        return Response({"message": "Account registered successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Authenticate user
        account = Account.objects.filter(username=username).first()
        if account and account.check_password(password):
            token, _ = Token.objects.get_or_create(user=account)
            return Response({
                "token": token.key,
                "username": account.username,
                "role": account.role,
                "employee_id": account.employee.id if account.employee else None
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class EmployeeList(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError as e:
            if 'phone_number' in str(e):
                raise ValidationError({'phone_number': 'Phone number already exists.'})
            if 'email' in str(e):
                raise ValidationError({'email': 'Email already exists.'})
            if 'citizen_id' in str(e):
                raise ValidationError({'citizen_id': 'Citizen identification already exists.'})
            raise ValidationError({'detail': 'An error occurred while creating the employee.'})

    def update(self, request, *args, **kwargs):
        employee = self.get_object()
        allowed_fields = ['phone_number', 'address', 'email', 'image', 'is_active']
        for field in allowed_fields:
            if field in request.data:
                setattr(employee, field, request.data[field])
        
        try:
            employee.save()
        except IntegrityError as e:
            if 'phone_number' in str(e):
                raise ValidationError({'phone_number': 'Phone number already exists.'})
            if 'email' in str(e):
                raise ValidationError({'email': 'Email already exists.'})
            raise ValidationError({'detail': 'An error occurred while updating the employee.'})

        serializer = self.get_serializer(employee)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        employee = self.get_object()
        employee.is_active = False
        employee.save()
        return Response({'message': 'Employee deactivated successfully'}, status=status.HTTP_200_OK)
    

class RoleListView(APIView):

    def get(self, request, *args, **kwargs):
        roles = [{'value': choice[0], 'label': choice[1]} for choice in Account._meta.get_field('role').choices]
        return Response({'roles': roles})


class ChangePasswordView(APIView):

    def post(self, request, pk=None):
        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            user = authenticate(username=employee.account.username, password=old_password)
            if user is None:
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            employee.account.password = make_password(new_password)
            employee.account.save()

            return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)