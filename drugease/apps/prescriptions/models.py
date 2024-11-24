from django.db import models
from apps.accounts.models import Employee

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.BooleanField()
    id_card = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='patients')

    class Meta:
        db_table = 'patient'

class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='prescribed_prescriptions')
    prescription_date = models.DateTimeField()
    usage_instructions = models.CharField(max_length=300)

    class Meta:
        db_table = 'prescription'

class PrescriptionDetail(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey('warehouse.Medicine', on_delete=models.CASCADE, related_name='prescription_details')
    quantity = models.IntegerField()

    class Meta:
        db_table = 'prescription_detail'
        unique_together = ('prescription', 'medicine')
