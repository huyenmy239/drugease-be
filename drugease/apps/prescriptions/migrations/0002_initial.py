# Generated by Django 5.1.3 on 2025-01-15 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prescriptions', '0001_initial'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescriptiondetail',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescription_details', to='warehouse.medicine'),
        ),
        migrations.AddField(
            model_name='prescriptiondetail',
            name='prescription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='prescriptions.prescription'),
        ),
        migrations.AlterUniqueTogether(
            name='prescriptiondetail',
            unique_together={('prescription', 'medicine')},
        ),
    ]
