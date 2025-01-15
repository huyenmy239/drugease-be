from rest_framework import serializers
from .models import Account,  Employee
from django.contrib.auth.hashers import check_password, make_password


def generate_id_card():
    last_employee = Employee.objects.last()
    if last_employee:
        last_id = last_employee.id
        new_id = last_id + 1
    else:
        new_id = 1
    return f"NV{new_id:03d}"

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'role', 'employee']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class EmployeeSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=['staff', 'doctor', 'pharmacist', 'admin'],
        write_only=True
    )
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id_card']


    def create(self, validated_data):
        validated_data['id_card'] = generate_id_card()
        validated_data['is_active'] = True
        
        role = validated_data.pop('role', 'staff')

        employee = employee = Employee.objects.create(**validated_data)

        account = Account.objects.create(
            username=employee.id_card,
            password=make_password(employee.phone_number),
            role=role,
            employee=employee
        )
        account.save()
        return employee


class EmployeeListSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField(source='account.username')
    role = serializers.StringRelatedField(source='account.role')

    class Meta:
        model = Employee
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)