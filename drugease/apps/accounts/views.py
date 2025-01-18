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
from django.db.models import Q
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
        if account:
            if not account.is_active:
                return Response(
                    {"error": "Account is inactive. Please contact the administrator."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
            

            if account.check_password(password):
                token, _ = Token.objects.get_or_create(user=account)
                return Response({
                    "token": token.key,
                    "username": account.username,
                    "role": account.role,
                    "employee_id": account.employee.id if account.employee else None
                }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class EmployeeList(APIView):
    permission_classes = [IsAuthenticated]
    # def get(self, request):
    #     employees = Employee.objects.all()
    #     serializer = EmployeeListSerializer(employees, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        query = request.query_params.get('query', None)  # Lấy tham số 'query'
        queryset = Employee.objects.all()

        if query:
            queryset = queryset.filter(
                Q(full_name__icontains=query) |
                Q(id_card__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(email__icontains=query)
            )

        serializer = EmployeeListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EmployeeListByRoleView(APIView):
    """
    APIView để lấy danh sách nhân viên theo role và is_active.
    """

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.query_params.get("role", None)

        if role is None:
            return Response(
                {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "status": "error",
                    "data": None,
                    "errorMessage": "role  parameters are required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        

        employees = Employee.objects.filter(
            account__role=role, is_active=True
        ).values("id", "full_name")

        data = list(employees)  # Convert QuerySet to list

        return Response(
            {
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": data,
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )


class EmployeeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
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
        
        serializer = self.get_serializer(employee, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee.save()

            if 'is_active' in request.data:
                account = getattr(employee, 'account', None)
            if account:
                account.is_active = employee.is_active
                account.save()

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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        roles = [{'value': choice[0], 'label': choice[1]} for choice in Account._meta.get_field('role').choices]
        return Response({'roles': roles})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

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


class EmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            employee = Employee.objects.get(account__username=pk)
            serializer = EmployeeProfileSerializer(employee, context={'request': request})
            return Response(serializer.data, status=200)
        except Employee.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
