from django.db import models
from apps.accounts.models import Employee
from apps.prescriptions.models import Prescription


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=False)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = "warehouse"


class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100, unique=True, null=False)
    unit = models.CharField(max_length=50, default="Viên")
    sale_price = models.FloatField(null=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="medicine_images/", blank=True, null=True)

    class Meta:
        db_table = "medicine"


class ImportReceipt(models.Model):
    id = models.AutoField(primary_key=True)
    import_date = models.DateTimeField(auto_now_add=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="import_receipts"
    )
    total_amount = models.FloatField(default=0)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="import_receipts"
    )
    is_approved = models.BooleanField(default=0)

    class Meta:
        db_table = "import_receipt"


class ImportReceiptDetail(models.Model):
    import_receipt = models.ForeignKey(
        ImportReceipt, on_delete=models.CASCADE, related_name="details"
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name="import_receipt_details"
    )
    quantity = models.IntegerField(null=False)
    price = models.FloatField(default=0)

    class Meta:
        db_table = "import_receipt_detail"
        unique_together = ("import_receipt", "medicine")


class ExportReceipt(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.FloatField(default=0)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="export_receipts"
    )
    export_date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="export_receipts"
    )
    prescription = models.OneToOneField(
        Prescription, on_delete=models.CASCADE, related_name="export_receipts"
    )
    is_approved = models.BooleanField(default=0)

    class Meta:
        db_table = "export_receipt"


class ExportReceiptDetail(models.Model):
    export_receipt = models.ForeignKey(
        ExportReceipt, on_delete=models.CASCADE, related_name="details"
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name="export_receipt_details"
    )
    quantity = models.IntegerField(null=False)
    price = models.FloatField(default=0)
    insurance_covered = models.BooleanField(default=True)
    ins_amount = models.FloatField(default=0)
    patient_pay = models.FloatField(default=0)

    class Meta:
        db_table = "export_receipt_detail"
        unique_together = ("export_receipt", "medicine")
