from datetime import datetime
from rest_framework import serializers
from .models import Patient, Prescription, PrescriptionDetail
from apps.accounts.models import Employee
from apps.warehouse.models import Medicine

class DoctorField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        return Employee.objects.filter(account__role='doctor')

class PatientSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'date_of_birth', 'gender', 'id_card', 'phone_number', 'address', 'email', 'insurance', 'registration_date', 'employee']

    def to_representation(self, instance):
        """
        Ghi đè to_representation để định dạng ngày theo dd/mm/yyyy khi trả về dữ liệu.
        """
        representation = super().to_representation(instance)
        
        if 'registration_date' in representation:
            representation['registration_date'] = instance.registration_date.strftime('%d/%m/%Y')
        if 'date_of_birth' in representation:
            representation['date_of_birth'] = instance.date_of_birth.strftime('%d/%m/%Y')
        
        return representation


class PatientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name']

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'medicine_name']

class PrescriptionDetailSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())  # Cho phép gửi ID khi POST
    medicine_name = serializers.ReadOnlyField(source='medicine.medicine_name')

    class Meta:
        model = PrescriptionDetail
        fields = ['id', 'prescription', 'medicine', 'medicine_name', 'quantity', 'usage_instruction']

    def validate_quantity(self, value):
        """Kiểm tra số lượng không âm hoặc bằng 0"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_usage_instruction(self, value):
        """Kiểm tra usage_instruction không quá 100 ký tự"""
        if value and len(value) > 100:
            raise serializers.ValidationError("Usage instruction must not exceed 100 characters.")
        return value

    def validate(self, data):
        """Kiểm tra toàn bộ dữ liệu PrescriptionDetail"""
        if not data.get('medicine'):
            raise serializers.ValidationError("Medicine is required.")
        if not data.get('prescription'):
            raise serializers.ValidationError("Prescription is required.")
        return data


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name']

class PrescriptionViewSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    details = PrescriptionDetailSerializer(many=True, read_only=True)
    patient = PatientNameSerializer()

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'prescription_date', 'instruction', 'details']

class PrescriptionDetailPostSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    quantity = serializers.IntegerField()
    usage_instruction = serializers.CharField()

    class Meta:
        model = PrescriptionDetail
        fields = ['medicine', 'quantity', 'usage_instruction']

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    diagnosis = serializers.CharField()
    prescription_date = serializers.DateField(required=False)
    details = PrescriptionDetailPostSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'prescription_date', 'instruction', 'details']

    def create(self, validated_data):
        # Kiểm tra xem có truyền prescription_date hay không, nếu không, gán giá trị mặc định
        prescription_date = validated_data.get('prescription_date', datetime.now().date())  # Sử dụng ngày hiện tại nếu không có giá trị

        # Tạo đơn thuốc với các dữ liệu đã validate và thêm prescription_date
        prescription = Prescription.objects.create(
            prescription_date=prescription_date,
            **validated_data
        )
        
        return prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = DoctorField(queryset=Employee.objects.all())
    details = PrescriptionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'prescription_date', 'instruction', 'details']

    def validate_diagnosis(self, value):
        """Kiểm tra diagnosis không quá 500 ký tự"""
        if len(value) > 500:
            raise serializers.ValidationError("Diagnosis must not exceed 500 characters.")
        return value

    def validate_instruction(self, value):
        """Kiểm tra instruction không quá 300 ký tự"""
        if len(value) > 300:
            raise serializers.ValidationError("Instruction must not exceed 300 characters.")
        return value

    def validate(self, data):
        """Kiểm tra bổ sung trên toàn bộ dữ liệu"""
        if not data.get('patient'):
            raise serializers.ValidationError("Patient is required.")
        if not data.get('doctor'):
            raise serializers.ValidationError("Doctor is required.")
        return data