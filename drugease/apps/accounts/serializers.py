from rest_framework import serializers
from .models import Account,  Employee
from django.contrib.auth.hashers import check_password, make_password
from datetime import date, timedelta

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
    

    def validate_full_name(self, value):
        """Kiểm tra full_name không được quá 50 ký tự và không rỗng"""
        if not value.strip():
            raise serializers.ValidationError("Full name cannot be empty.")
        if len(value) > 50:
            raise serializers.ValidationError("Full name must not exceed 50 characters.")
        return value

    def validate_date_of_birth(self, value):
        """Kiểm tra ngày sinh không được là tương lai và người dùng phải đủ 18 tuổi"""
        today = date.today()
        min_age_date = today - timedelta(days=18*365)  # Cách tính đủ 18 tuổi (ước lượng 365 ngày mỗi năm)

        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        if value > min_age_date:
            raise serializers.ValidationError("Employee must be at least 18 years old.")
        
        return value

    def validate_phone_number(self, value):
        """Kiểm tra định dạng số điện thoại"""
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10 or len(value) > 11:
            raise serializers.ValidationError("Phone number must be between 10 and 11 digits.")
        return value

    def validate_email(self, value):
        """Kiểm tra email không rỗng và định dạng hợp lệ"""
        if not value.strip():
            raise serializers.ValidationError("Email cannot be empty.")
        return value

    def validate_citizen_id(self, value):
        """Kiểm tra citizen_id có độ dài chính xác"""
        if len(value) != 12:
            raise serializers.ValidationError("Citizen ID must be exactly 12 characters.")
        if not value.isdigit():
            raise serializers.ValidationError("Citizen ID must contain only digits.")
        return value

    def validate(self, data):
        """Kiểm tra tính logic giữa các trường"""
        if 'gender' in data and data['gender'] not in [True, False]:
            raise serializers.ValidationError({"gender": "Gender must be either True (Male) or False (Female)."})
        return data


class EmployeeListSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField(source='account.username')
    role = serializers.StringRelatedField(source='account.role')

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeProfileSerializer(serializers.ModelSerializer):
    account = serializers.CharField(source='account.username', read_only=True)
    role = serializers.CharField(source='account.role', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)