from rest_framework import serializers
from .models import Patient, Prescription, PrescriptionDetail
from apps.accounts.models import Employee
from apps.warehouse.models import Medicine


class DoctorField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        return Employee.objects.filter(account__role='doctor')

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'date_of_birth', 'gender', 'id_card', 'phone_number', 'address', 'email', 'registration_date', 'insurance', 'employee']

    def update(self, instance, validated_data):
        email = validated_data.get('email', instance.email)
        phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = email
        instance.phone_number = phone_number
        instance.save()
        return instance


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


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = DoctorField(queryset=Employee.objects.all())
    details = PrescriptionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'prescription_date', 'instruction', 'details']