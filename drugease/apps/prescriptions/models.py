from django.db import models
from apps.accounts.models import Employee

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.BooleanField(default=0)
    id_card = models.CharField(max_length=12, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    insurance = models.FloatField(default=0.0)
    nguoi_giam_ho = models.CharField(max_length=50, default="Không có");
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='patients')

    class Meta:
        db_table = 'patient'

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='prescribed_prescriptions')
    diagnosis = models.CharField(max_length=500)
    prescription_date = models.DateTimeField(auto_now_add=True)
    instruction = models.CharField(max_length=300, default="")

    class Meta:
        db_table = 'prescription'

class PrescriptionDetail(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey('warehouse.Medicine', on_delete=models.CASCADE, related_name='prescription_details')
    quantity = models.IntegerField()
    usage_instruction = models.CharField(max_length=100,  null=True, blank=True)

    class Meta:
        db_table = 'prescription_detail'
        unique_together = ('prescription', 'medicine')
