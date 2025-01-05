from rest_framework import serializers
from .models import Medicine, ImportReceiptDetail
from apps.prescriptions.models import PrescriptionDetail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import *


# view for Medicine
class MedicineListView(APIView):
    def get(self, request):
        medicines = Medicine.objects.all()
        data = [
            {
                "id": medicine.id,
                "medicine_name": medicine.medicine_name,
                "unit": medicine.unit,
                "sale_price": medicine.sale_price,
                "description": medicine.description,
                "stock_quantity": medicine.stock_quantity,
                "employee_id": medicine.employee.id,
            }
            for medicine in medicines
        ]
        return Response(
            {
                "statuscode": status.HTTP_200_OK,
                "data": None,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_201_CREATED,
        )


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            medicine_name = request.data.get("medicine_name")
            unit = request.data.get("unit")
            sale_price = request.data.get("sale_price")
            total_amount = request.data.get("total_amount")
            if not medicine_name.strip():
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Không được bỏ trống tên thuốc.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not unit.strip():
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Không được bỏ trống đơn vị tính.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if int(sale_price) <= 0:
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Giá thuốc phải lớn hơn 0.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if int(total_amount) <= 0:
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Số lượng tồn phải lớn hơn 0.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Medicine.objects.filter(medicine_name=medicine_name).exists():
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Tên thuốc này đã tồn tại.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "statuscode": status.HTTP_201_CREATED,
                        "data": serializer.data,
                        "status": "success",
                        "errorMessage": None,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {
                    "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": None,
                    "status": "error",
                    "errorMessage": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            serializer = self.get_serializer(instance, data=request.data)

            unit = request.data.get("unit", "")
            sale_price = request.data.get("sale_price", 0)

            if not unit.strip():
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Không được bỏ trống đơn vị tính.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if sale_price <= 0:
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Giá thuốc phải lớn hơn 0.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if serializer.is_valid():

                serializer.save()
                return Response(
                    {
                        "statuscode": status.HTTP_200_OK,
                        "data": serializer.data,
                        "status": "success",
                        "errorMessage": None,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {
                    "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": None,
                    "status": "error",
                    "errorMessage": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if ImportReceiptDetail.objects.filter(medicine=instance).exists():
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Thuốc này không thể xóa vì đã tồn tại trong phiếu nhập.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if PrescriptionDetail.objects.filter(medicine=instance).exists():
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Thuốc này không thể xóa vì đã tồn tại trong phiếu xuất.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            instance.delete()
            return Response(
                {
                    "statuscode": status.HTTP_204_NO_CONTENT,
                    "data": None,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            return Response(
                {
                    "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": None,
                    "status": "error",
                    "errorMessage": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# view for Warehouse
class WarehouseListAPIView(APIView):
    """
    API endpoint để xem danh sách kho hàng với khả năng tìm kiếm.
    """

    def get(self, request):
        warehouses = Warehouse.objects.all()

        data = [
            {
                "id": warehouse.id,
                "warehouse_name": warehouse.warehouse_name,
                "address": warehouse.address,
                "is_active": warehouse.is_active,
            }
            for warehouse in warehouses
        ]

        return Response(
            {
                "statuscode": status.HTTP_200_OK,
                "data": data,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        """
        Override this method to add search functionality.
        """
        queryset = Warehouse.objects.all()
        search_query = self.request.query_params.get("q", None)
        if search_query:
            queryset = queryset.filter(warehouse_name__icontains=search_query)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle custom validation if needed.
        """
        warehouse_name = request.data.get("warehouse_name")
        address = request.data.get("address")

        print("is active", request.data.get("is_active"))
        # Kiểm tra tên kho không được trống
        check_response = check_not_empty(warehouse_name, "tên kho")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        # Kiểm tra địa chỉ không được trống
        check_response = check_not_empty(address, "địa chỉ kho")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ
        check_response = WarehouseSerializer.check_warehouse_name_exists(warehouse_name)
        if check_response:
            return check_response
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "statuscode": status.HTTP_201_CREATED,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        """
        Override the update method to handle partial or full updates.
        """
        instance = self.get_object()
        print("instance", instance.is_active)
        warehouse_name = request.data.get("warehouse_name")
        address = request.data.get("address")
        # Kiểm tra tên kho không được trống
        check_response = check_not_empty(warehouse_name, "tên kho")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        # Kiểm tra địa chỉ không được trống
        check_response = check_not_empty(address, "địa chỉ kho")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ
        check_response = WarehouseSerializer.check_warehouse_name_exists(
            warehouse_name, current_warehouse=instance
        )
        if check_response:
            return check_response
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            print("is active", request.data.get("is_active"))

            serializer.save()
            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to handle deletion.
        """
        instance = self.get_object()
        if ImportReceipt.objects.filter(warehouse=instance).exists():
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Kho này không thể xóa vì đã tồn tại trong phiếu nhập.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if ExportReceipt.objects.filter(warehouse=instance).exists():
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Kho này không thể xóa vì đã tồn tại trong phiếu xuất.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
        return Response(
            {
                "statuscode": status.HTTP_204_NO_CONTENT,
                "data": None,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


# view for ImportReceipt

class ImportReceiptListAPIView(APIView):
    """
    API endpoint để xem danh sách phiếu nhập với khả năng tìm kiếm.
    """

    def get(self, request):
        import_receipts = ImportReceipt.objects.all()
        search_query = request.query_params.get("q", None)
        if search_query:
            import_receipts = import_receipts.filter(warehouse__warehouse_name__icontains=search_query)

        data = [
            {
                "id": receipt.id,
                "import_date": receipt.import_date.strftime("%d/%m/%Y %H:%M"),
                "warehouse_name": receipt.warehouse.warehouse_name,
                "total_amount": receipt.total_amount,
                "employee_name": receipt.employee.name,
                "is_approved": receipt.is_approved,
            }
            for receipt in import_receipts
        ]

        return Response(
            {
                "statuscode": status.HTTP_200_OK,
                "data": data,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )

class ImportReceiptViewSet(viewsets.ModelViewSet):
    queryset = ImportReceipt.objects.all()
    serializer_class = ImportReceiptSerializer

    def get_queryset(self):
        """
        Tìm kiếm theo tên kho và theo ngày nhập.
        """
        queryset = ImportReceipt.objects.all()
        search_query = self.request.query_params.get("q", None)
        if search_query:
            queryset = queryset.filter(
                warehouse__warehouse_name__icontains=search_query
            )
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Tạo mới ImportReceipt
        """
        warehouse = request.data.get("warehouse")
        import_date = request.data.get("import_date")
        total_amount = request.data.get("total_amount")
        employee = request.data.get("employee")

        # Kiểm tra các trường không trống
        check_response = check_not_empty(warehouse, "Kho")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        check_response = check_not_empty(import_date, "Ngày nhập")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        check_response = check_not_empty(total_amount, "Tổng tiền")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        check_response = check_not_empty(employee, "Nhân viên")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "statuscode": status.HTTP_201_CREATED,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        """
        Cập nhật ImportReceipt
        """
        instance = self.get_object()
        warehouse = request.data.get("warehouse")
        import_date = request.data.get("import_date")
        total_amount = request.data.get("total_amount")
        employee = request.data.get("employee")

        # Kiểm tra các trường không trống
        check_response = check_not_empty(warehouse, "Kho")
        if check_response:
            return check_response

        check_response = check_not_empty(import_date, "Ngày nhập")
        if check_response:
            return check_response

        check_response = check_not_empty(total_amount, "Tổng tiền")
        if check_response:
            return check_response

        check_response = check_not_empty(employee, "Nhân viên")
        if check_response:
            return check_response
        if instance.is_approved:
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Không thể sửa phiếu nhập đã được phê duyệt.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Xóa ImportReceipt
        """
        instance = self.get_object()
        if instance.is_approved:
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Không thể xóa phiếu nhập đã được phê duyệt.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
        return Response(
            {
                "statuscode": status.HTTP_204_NO_CONTENT,
                "data": None,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class ImportReceiptDetailAPIView(APIView):
    """
    API endpoint để xem chi tiết một phiếu nhập.
    """

    def get(self, request, pk):
        try:
            receipt = ImportReceipt.objects.get(pk=pk)
        except ImportReceipt.DoesNotExist:
            return Response(
                {
                    "statuscode": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Phiếu nhập không tồn tại.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        details = ImportReceiptDetail.objects.filter(import_receipt=receipt)
        detail_data = [
            {
                "medicine_name": detail.medicine.name,
                "quantity": detail.quantity,
                "price": detail.price,
            }
            for detail in details
        ]

        # data = {
        #     "id": receipt.id,
        #     "import_date": receipt.import_date,
        #     "warehouse_name": receipt.warehouse.warehouse_name,
        #     "total_amount": receipt.total_amount,
        #     "employee_name": receipt.employee.name,
        #     "is_approved": receipt.is_approved,
        #     "details": detail_data,
        # }

        return Response(
            {
                "statuscode": status.HTTP_200_OK,
                "data": detail_data,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )


class ImportReceiptDetailViewSet(viewsets.ModelViewSet):
    queryset = ImportReceiptDetail.objects.all()
    serializer_class = ImportReceiptDetailSerializer

    def get_queryset(self):
        """
        Tìm kiếm theo mã thuốc hoặc tên thuốc
        """
        queryset = ImportReceiptDetail.objects.all()
        search_query = self.request.query_params.get("q", None)
        if search_query:
            queryset = queryset.filter(medicine__name__icontains=search_query)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Tạo mới ImportReceiptDetail
        """
        import_receipt = request.data.get("import_receipt")
        medicine = request.data.get("medicine")
        quantity = request.data.get("quantity")
        price = request.data.get("price")

        # Kiểm tra các trường không trống
        check_response = check_not_empty(import_receipt, "Phiếu nhập")
        if check_response:
            return check_response

        check_response = check_not_empty(medicine, "Thuốc")
        if check_response:
            return check_response

        check_response = check_not_empty(quantity, "Số lượng")
        if check_response:
            return check_response

        check_response = check_not_empty(price, "Giá")
        if check_response:
            return check_response


        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "statuscode": status.HTTP_201_CREATED,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        """
        Cập nhật ImportReceiptDetail
        """
        instance = self.get_object()

        import_receipt = request.data.get("import_receipt", instance.import_receipt.id)
        medicine = request.data.get("medicine", instance.medicine.id)
        quantity = request.data.get("quantity", instance.quantity)
        price = request.data.get("price", instance.price)

        # Kiểm tra các trường không trống
        check_response = check_not_empty(import_receipt, "Phiếu nhập")
        if check_response:
            return check_response

        check_response = check_not_empty(medicine, "Thuốc")
        if check_response:
            return check_response

        check_response = check_not_empty(quantity, "Số lượng")
        if check_response:
            return check_response

        check_response = check_not_empty(price, "Giá")
        if check_response:
            return check_response

        # Cập nhật dữ liệu
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    def destroy(self, request, *args, **kwargs):
        """
        Xóa ImportReceiptDetail, kiểm tra nếu ImportReceipt đã được phê duyệt thì không cho phép xóa.
        """
        instance = self.get_object()

        # Kiểm tra nếu phiếu nhập đã được phê duyệt
        if instance.import_receipt.is_approved:
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Không thể xóa chi tiết phiếu nhập đã được phê duyệt.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Xóa chi tiết phiếu nhập
        instance.delete()
        return Response(
            {
                "statuscode": status.HTTP_204_NO_CONTENT,
                "data": None,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )
