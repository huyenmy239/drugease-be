from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(null=False)
    gender = models.BooleanField(default=0)
    id_card = models.CharField(max_length=12, unique=True, null=False)
    phone_number = models.CharField(max_length=12, null=False)
    address = models.CharField(max_length=200, null=False)
    email = models.EmailField(unique=True, null=False)
    image = models.TextField(null=True, blank=True) # Add default image later
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = 'employee'

from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(AbstractUser):
    role = models.CharField(max_length=50, choices=[
        ('doctor', 'Doctor'),
        ('pharmacist', 'Pharmacist'),
        ('admin', 'Admin'),
        ('staff', 'Staff')
    ])
    employee = models.OneToOneField('accounts.Employee', on_delete=models.CASCADE, related_name='account', null=True, blank=True)

    email = None
    last_login = None
    is_superuser = None
    first_name = None
    last_name = None
    is_staff = None
    date_joined = None

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'account'
