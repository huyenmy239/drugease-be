from django.db import models
from apps.accounts.models import Employee
from apps.prescriptions.models import Prescription

class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    is_active = models.BooleanField(default=1)

    class Meta:
        db_table = 'warehouse'

class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50)
    sale_price = models.FloatField()
    description = models.CharField(max_length=200)
    stock_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'medicine'

class ImportReceipt(models.Model):
    id = models.AutoField(primary_key=True)
    import_date = models.DateTimeField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='import_receipts')
    total_amount = models.FloatField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='import_receipts')
    is_approved = models.BooleanField(default=0)

    class Meta:
        db_table = 'import_receipt'

class ImportReceiptDetail(models.Model):
    import_receipt = models.ForeignKey(ImportReceipt, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='import_receipt_details')
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        db_table = 'import_receipt_detail'
        unique_together = ('import_receipt', 'medicine')

class ExportReceipt(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.FloatField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='export_receipts')
    export_date = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='export_receipts')
    prescription = models.OneToOneField(Prescription, on_delete=models.CASCADE, related_name='export_receipts')
    is_approved = models.BooleanField(default=0)

    class Meta:
        db_table = 'export_receipt'

class ExportReceiptDetail(models.Model):
    export_receipt = models.ForeignKey(ExportReceipt, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='export_receipt_details')
    quantity = models.IntegerField()
    price = models.FloatField()
    insurance_covered = models.BooleanField(default=True)
    ins_amount = models.FloatField(default=0)
    patient_pay = models.FloatField(default=0)

    class Meta:
        db_table = 'export_receipt_detail'
        unique_together = ('export_receipt', 'medicine')
