<<<<<<< HEAD
# Generated by Django 5.1.3 on 2025-01-14 07:03
=======
# Generated by Django 5.1.3 on 2025-01-15 01:06
>>>>>>> d7b4ddd4300ba076f55c7a5ca429306673aff4f4

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("prescriptions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Medicine",
            fields=[

                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("medicine_name", models.CharField(max_length=100, unique=True)),
                ("unit", models.CharField(default="Viên", max_length=50)),
                ("sale_price", models.FloatField()),
                (
                    "description",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("stock_quantity", models.IntegerField(default=0)),
                ("image", models.TextField(blank=True, null=True)),

            ],
            options={
                "db_table": "medicine",
            },
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("warehouse_name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=200)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "warehouse",
            },
        ),
        migrations.CreateModel(
            name="ExportReceipt",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("total_amount", models.FloatField(default=0)),
                ("export_date", models.DateTimeField(auto_now_add=True)),
                ("is_approved", models.BooleanField(default=0)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="export_receipts",
                        to="accounts.employee",
                    ),
                ),
                (
                    "prescription",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="export_receipts",
                        to="prescriptions.prescription",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="export_receipts",
                        to="warehouse.warehouse",
                    ),
                ),
            ],
            options={
                "db_table": "export_receipt",
            },
        ),
        migrations.CreateModel(
            name="ImportReceipt",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("import_date", models.DateTimeField(auto_now_add=True)),
                ("total_amount", models.FloatField(default=0)),
                ("is_approved", models.BooleanField(default=0)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="import_receipts",
                        to="accounts.employee",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="import_receipts",
                        to="warehouse.warehouse",
                    ),
                ),
            ],
            options={
                "db_table": "import_receipt",
            },
        ),
        migrations.CreateModel(
            name="ImportReceiptDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("price", models.FloatField(default=0)),
                (
                    "import_receipt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="warehouse.importreceipt",
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="import_receipt_details",
                        to="warehouse.medicine",
                    ),
                ),
            ],
            options={
                "db_table": "import_receipt_detail",
                "unique_together": {("import_receipt", "medicine")},
            },
        ),
        migrations.CreateModel(
            name="ExportReceiptDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("price", models.FloatField(default=0)),
                ("insurance_covered", models.BooleanField(default=True)),
                ("ins_amount", models.FloatField(default=0)),
                ("patient_pay", models.FloatField(default=0)),
                (
                    "export_receipt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="warehouse.exportreceipt",
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="export_receipt_details",
                        to="warehouse.medicine",
                    ),
                ),
            ],
            options={
                "db_table": "export_receipt_detail",
                "unique_together": {("export_receipt", "medicine")},
            },
        ),
    ]
