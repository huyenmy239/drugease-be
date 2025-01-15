# Generated by Django 5.1.3 on 2025-01-14 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrescriptionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('usage_instruction', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'prescription_detail',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.BooleanField(default=0)),
                ('id_card', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('phone_number', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('insurance', models.FloatField(default=0.0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='accounts.employee')),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('diagnosis', models.CharField(max_length=500)),
                ('prescription_date', models.DateTimeField(auto_now_add=True)),
                ('instruction', models.CharField(default='', max_length=300)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescribed_prescriptions', to='accounts.employee')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='prescriptions.patient')),
            ],
            options={
                'db_table': 'prescription',
            },
        ),
    ]
