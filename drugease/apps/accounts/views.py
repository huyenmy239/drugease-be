from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from .models import Account, Employee
from .serializers import AccountSerializer, LoginSerializer


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
