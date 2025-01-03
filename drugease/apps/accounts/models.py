from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.BooleanField(default=0)
    id_card = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    image = models.TextField()
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
