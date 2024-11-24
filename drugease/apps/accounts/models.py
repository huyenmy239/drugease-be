from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=60)
    date_of_birth = models.DateField()
    gender = models.BooleanField()
    id_card = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    image = models.TextField()

    class Meta:
        db_table = 'employee'

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    role = models.CharField(max_length=50)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='account')

    class Meta:
        db_table = 'account'
