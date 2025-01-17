from rest_framework import serializers
from apps.prescriptions.models import Patient

class PatientReportSerializer(serializers.ModelSerializer):
    gender = serializers.CharField()
    age = serializers.IntegerField()

    class Meta:
        model = Patient
        fields = ['id', 'gender', 'registration_date']