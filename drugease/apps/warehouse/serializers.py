from rest_framework import serializers
from .models import (
    Medicine,
    Warehouse,
    ImportReceipt,
    ImportReceiptDetail,
    ExportReceipt,
    ExportReceiptDetail,
)
from apps.accounts.models import Employee

from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


def check_not_empty(value, field_name):
    """
    Kiểm tra giá trị không rỗng và không chỉ chứa khoảng trắng.
    Nếu không hợp lệ, trả về Response với lỗi.

    :param value: Giá trị cần kiểm tra.
    :param field_name: Tên trường để hiển thị trong thông báo lỗi.
    :return: None nếu giá trị hợp lệ, hoặc Response với lỗi nếu không hợp lệ.
    """
    if not value or not value.strip():
        return Response(
            {
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": f"Không được bỏ trống {field_name}.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None


##Serializer for Medicine
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"

    # def check_medicine_name(value):
    #     """Kiểm tra tính hợp lệ cho trường 'medicine_name'."""
    #     if not value:
    #         raise serializers.ValidationError("Tên thuốc không được bỏ trống.")
    #     elif len(value) < 3:
    #         raise serializers.ValidationError("Tên thuốc phải có ít nhất 3 ký tự.")
    #     return value

    # def check_sale_price(value):
    #     """Kiểm tra tính hợp lệ cho trường 'sale_price'."""
    #     if not value:
    #         raise serializers.ValidationError("Không được bỏ trống giá thuốc.")
    #     elif value <= 0:
    #         raise serializers.ValidationError("Giá thuốc phải lớn hơn 0.")
    #     return value

    # def check_stock_quantity(value):
    #     """Kiểm tra tính hợp lệ cho trường 'stock_quantity'."""
    #     if value < 0:
    #         raise serializers.ValidationError("Số lượng thuốc không thể nhỏ hơn 0.")
    #     return value

    # def check_unit(value):
    #     """Kiểm tra tính hợp lệ cho trường 'unit'."""
    #     if not value or value == "":
    #         raise serializers.ValidationError("Không được bỏ trống đơn vị tính.")
    #     return value


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"

    def check_warehouse_name_exists(value, current_warehouse=None):
        """
        Kiểm tra xem tên kho đã tồn tại trong cơ sở dữ liệu chưa.
        Nếu có, trả về Response với lỗi.
        Nếu đang cập nhật, kiểm tra xem tên kho có trùng với kho khác không, ngoại trừ kho hiện tại.

        :param value: Tên kho cần kiểm tra.
        :param current_warehouse: Kho hiện tại, dùng trong trường hợp cập nhật.
        :return: None nếu không trùng lặp, hoặc Response với lỗi nếu trùng lặp.
        """
        if current_warehouse:
            # Khi đang cập nhật, kiểm tra tên kho có trùng với kho khác không, ngoại trừ kho hiện tại
            if (
                Warehouse.objects.filter(warehouse_name__iexact=value)
                .exclude(id=current_warehouse.id)
                .exists()
            ):
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Tên kho đã tồn tại.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Khi tạo mới, chỉ kiểm tra tên kho có tồn tại hay không
            if Warehouse.objects.filter(warehouse_name__iexact=value).exists():
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Tên kho đã tồn tại.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return None


class ImportReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportReceipt
        fields = "__all__"  # Hoặc chọn các trường bạn muốn trả về


class ImportReceiptDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportReceiptDetail
        fields = "__all__"  # Hoặc chọn các trường bạn muốn trả về


class IRDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportReceiptDetail
        fields = [
            "medicine",
            "quantity",
            "price",
        ]  # Hoặc chọn các trường bạn muốn trả về


class ImportReceiptAndDetailSerializer(serializers.ModelSerializer):
    details = IRDetailSerializer(many=True)

    class Meta:
        model = ImportReceipt
        fields = ["warehouse", "total_amount", "employee", "is_approved", "details"]

    def create(self, validated_data):
        """
        Tạo phiếu nhập và chi tiết phiếu nhập trong một giao dịch.
        """
        details_data = validated_data.pop(
            "details"
        )  # Tách chi tiết phiếu nhập từ validated_data
        import_receipt = ImportReceipt.objects.create(
            **validated_data
        )  # Tạo phiếu nhập

        # Tạo các chi tiết phiếu nhập
        for detail_data in details_data:
            ImportReceiptDetail.objects.create(
                import_receipt=import_receipt, **detail_data
            )

        return import_receipt

    def update_stock_quantity(self, import_receipt):
        """
        Cập nhật stock_quantity của medicine khi phiếu nhập được phê duyệt.
        """
        if import_receipt.is_approved:
            for detail in import_receipt.details.all():
                medicine = detail.medicine
                medicine.stock_quantity += detail.quantity  # Cộng thêm số lượng vào kho
                medicine.save()
