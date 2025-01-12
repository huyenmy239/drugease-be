from rest_framework import serializers
from .models import Medicine, ImportReceiptDetail
from apps.prescriptions.models import PrescriptionDetail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
import base64
from io import BytesIO
from PIL import Image
from django.db.models import Q
from datetime import datetime
from rest_framework.decorators import action


# view for Medicine
class MedicineListView(APIView):
    def get(self, request):
        medicines = Medicine.objects.all()

        # In ra toàn bộ danh sách thuốc
        print("Medicines fetched from DB:", medicines)

        data = []
        for medicine in medicines:
            print(
                f"Processing medicine: {medicine.medicine_name}"
            )  # In ra tên thuốc trước khi xử lý

            # Kiểm tra xem thuốc có hình ảnh hay không
            if medicine.image:
                try:
                    print(f"Medicine {medicine.medicine_name} has an image.")
                    img = Image.open(medicine.image.path)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    image_data = f"data:image/png;base64,{img_str}"
                except Exception as e:
                    print(f"Error converting image to base64: {e}")
                    image_data = None
            else:
                print(f"Medicine {medicine.medicine_name} does not have an image.")
                image_data = None

            # Thêm thông tin thuốc vào danh sách
            data.append(
                {
                    "id": medicine.id,
                    "medicine_name": medicine.medicine_name,
                    "unit": medicine.unit,
                    "sale_price": medicine.sale_price,
                    "description": medicine.description,
                    "stock_quantity": medicine.stock_quantity,
                    "image": image_data,
                }
            )

        # In ra kết quả trước khi trả về Response
        print("Final data to be returned:", data)

        return Response(
            {
                "statuscode": status.HTTP_200_OK,
                "data": data,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            medicine_name = request.data.get("medicine_name")
            unit = request.data.get("unit")
            sale_price = request.data.get("sale_price")
            total_amount = request.data.get("stock_quantity")
            print("request.data", request.data)
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
            print("total_amount", type(total_amount))
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
                print("serializer.data", serializer.data)
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
            print("request", request.data)
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


class WarehouseDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            # Lấy chi tiết kho theo ID (pk)
            warehouse = Warehouse.objects.get(pk=pk)
            serializer = WarehouseSerializer(warehouse)

            # Tạo response JSON
            response = {
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": serializer.data,
                "errorMessage": None,
            }
            return Response(response, status=status.HTTP_200_OK)

        except Warehouse.DoesNotExist:
            # Trả về lỗi nếu kho không tồn tại
            response = {
                "statusCode": status.HTTP_404_NOT_FOUND,
                "status": "error",
                "data": None,
                "errorMessage": "Warehouse not found.",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Trả về lỗi cho các trường hợp ngoại lệ khác
            response = {
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "status": "error",
                "data": None,
                "errorMessage": str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Tìm kiếm kho theo địa chỉ và trạng thái is_active.
        """
        # Lấy các tham số từ query params
        address = request.query_params.get('address', None)
        is_active = request.query_params.get('is_active', None)

        # Lọc dữ liệu
        warehouses = Warehouse.objects.all()
        if address:
            warehouses = warehouses.filter(address__icontains=address)
        if is_active is not None:
            warehouses = warehouses.filter(is_active=is_active.lower() == 'true')

        # Serialize dữ liệu
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response({
            "statusCode": status.HTTP_200_OK,
            "status": "success",
            "data": serializer.data,
            "errorMessage": None,
        }, status=status.HTTP_200_OK)
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
        # search_query = request.query_params.get("q", None)
        # if search_query:
        #     import_receipts = import_receipts.filter(warehouse__warehouse_name__icontains=search_query)

        data = [
            {
                "id": receipt.id,
                "import_date": receipt.import_date.strftime("%d/%m/%Y %H:%M"),
                "warehouse_name": receipt.warehouse.warehouse_name,
                "total_amount": receipt.total_amount,
                "employee_name": receipt.employee.full_name,
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


class ImportReceiptCreateView(CreateAPIView):
    queryset = ImportReceipt.objects.all()
    serializer_class = ImportReceiptAndDetailSerializer

    def create(self, request, *args, **kwargs):
        # Xử lý yêu cầu POST để tạo phiếu nhập và chi tiết phiếu nhập
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Tạo và lưu phiếu nhập và chi tiết phiếu nhập
            import_receipt = serializer.save()
            response = {
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": serializer.data,
                "errorMessage": None,
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response(
            {
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ImportReceiptAPIView(APIView):
    def get(self, request, pk):
        try:
            # Lấy biên bản nhập kho theo ID (pk)
            import_receipt = ImportReceipt.objects.get(pk=pk)
            
            # Chuẩn bị dữ liệu tùy chỉnh
            receipt_data = {
                "id": import_receipt.id,
                "import_date": import_receipt.import_date.strftime("%d/%m/%Y %H:%M"),
                "warehouse": import_receipt.warehouse.warehouse_name,  # Tên kho
                "total_amount": import_receipt.total_amount,  # Tổng giá trị
                "employee": import_receipt.employee.full_name,  # Tên nhân viên
                "is_approved": import_receipt.is_approved,  # Trạng thái duyệt
            }

            # Tạo response JSON
            response = {
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": receipt_data,
                "errorMessage": None,
            }
            return Response(response, status=status.HTTP_200_OK)

        except ImportReceipt.DoesNotExist:
            # Trả về lỗi nếu biên bản nhập kho không tồn tại
            response = {
                "statusCode": status.HTTP_404_NOT_FOUND,
                "status": "error",
                "data": None,
                "errorMessage": "Import receipt not found.",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Trả về lỗi cho các trường hợp ngoại lệ khác
            response = {
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "status": "error",
                "data": None,
                "errorMessage": str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Custom action to search import receipts by criteria.
        """
        try:
            # Retrieve query parameters
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            employee_name = request.query_params.get("employee_name")
            warehouse_name = request.query_params.get("warehouse_name")
            is_approved = request.query_params.get("is_approved")

            # Build query
            query = Q()

            if start_date:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                query &= Q(import_date__gte=start_date_obj)

            if end_date:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                query &= Q(import_date__lte=end_date_obj)

            if employee_name:
                query &= Q(employee__full_name__icontains=employee_name)

            if warehouse_name:
                query &= Q(warehouse__warehouse_name__icontains=warehouse_name)

            if is_approved is not None:
                is_approved_bool = is_approved.lower() == "true"
                query &= Q(is_approved=is_approved_bool)

            # Filter data
            import_receipts = ImportReceipt.objects.filter(query)

            # Serialize data
            data = [
                {
                    "id": receipt.id,
                    "import_date": receipt.import_date.strftime("%d/%m/%Y %H:%M"),
                    "warehouse_name": receipt.warehouse.warehouse_name,
                    "total_amount": receipt.total_amount,
                    "employee_name": receipt.employee.full_name,
                    "is_approved": receipt.is_approved,
                }
                for receipt in import_receipts
            ]

            return Response(
                {
                    "statusCode": status.HTTP_200_OK,
                    "status": "success",
                    "data": data,
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "status": "error",
                    "data": None,
                    "errorMessage": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

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

        # check_response = check_not_empty(import_date, "Ngày nhập")
        # if check_response:
        #     return check_response  # Trả về lỗi nếu không hợp lệ

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
        print("is import_date", instance.import_date)
        warehouse = request.data.get("warehouse")
        import_date = request.data.get("import_date")
        total_amount = request.data.get("total_amount")
        employee = request.data.get("employee")

        # Kiểm tra các trường không trống
        check_response = check_not_empty(warehouse, "Kho")
        if check_response:
            return check_response

        # check_response = check_not_empty(import_date, "Ngày nhập")
        # if check_response:
        #     return check_response

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


# class ImportReceiptDetailListAPIView(APIView):
#     """
#     API endpoint để xem tất cả chi tiết của các phiếu nhập.
#     """

#     def get(self, request):
#         try:
#             details = ImportReceiptDetail.objects.all()
#             detail_data = [
#                 {
#                     "import_receipt_id": detail.import_receipt.id,
#                     "medicine_name": detail.medicine.medicine_name,
#                     "quantity": detail.quantity,
#                     "price": detail.price,
#                 }
#                 for detail in details
#             ]

#             return Response(
#                 {
#                     "statuscode": status.HTTP_200_OK,
#                     "data": detail_data,
#                     "status": "success",
#                     "errorMessage": None,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except ImportReceiptDetail.DoesNotExist:
#             return Response(
#                 {
#                     "statuscode": status.HTTP_404_NOT_FOUND,
#                     "data": None,
#                     "status": "error",
#                     "errorMessage": "Không tìm thấy chi tiết phiếu nhập nào.",
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     "data": None,
#                     "status": "error",
#                     "errorMessage": f"Đã xảy ra lỗi: {str(e)}",
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


class ImportReceiptDetailsByIdAPIView(APIView):
    """
    API endpoint để xem tất cả chi tiết của các phiếu nhập hoặc chi tiết theo ID phiếu nhập.
    """

    def get(self, request, pk=None):
        try:
            if pk:
                # Lấy chi tiết cho phiếu nhập cụ thể
                details = ImportReceiptDetail.objects.filter(import_receipt__id=pk)
                if not details.exists():
                    return Response(
                        {
                            "statuscode": status.HTTP_404_NOT_FOUND,
                            "data": None,
                            "status": "error",
                            "errorMessage": "Không tìm thấy chi tiết cho phiếu nhập với ID đã cung cấp.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                # Lấy tất cả chi tiết
                details = ImportReceiptDetail.objects.all()

            detail_data = [
                {
                    "import_receipt": detail.import_receipt.id,
                    "medicine": detail.medicine.id,
                    "quantity": detail.quantity,
                    "price": detail.price,
                }
                for detail in details
            ]

            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": detail_data,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": None,
                    "status": "error",
                    "errorMessage": f"Đã xảy ra lỗi: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk):
        """
        Cập nhật nhiều chi tiết phiếu nhập cho phiếu nhập cụ thể.
        """
        try:
            receipt = ImportReceipt.objects.get(pk=pk)
            details = request.data.get("details", [])

            updated_details = []
            for detail in details:
                medicine_id = detail.get("medicine")
                quantity = detail.get("quantity")
                price = detail.get("price")

                # Get the Medicine instance using medicine_id
                medicine_instance = Medicine.objects.get(id=medicine_id)

                try:
                    # Try to get the existing ImportReceiptDetail
                    import_receipt_detail = ImportReceiptDetail.objects.get(
                        medicine=medicine_instance, import_receipt=receipt
                    )
                    # If found, update it
                    import_receipt_detail.quantity = quantity
                    import_receipt_detail.price = price
                    import_receipt_detail.save()

                    updated_details.append(
                        {
                            "import_receipt": receipt.id,
                            "medicine": import_receipt_detail.medicine.id,
                            "quantity": import_receipt_detail.quantity,
                            "price": import_receipt_detail.price,
                        }
                    )

                except ImportReceiptDetail.DoesNotExist:
                    # If no existing detail found, create a new one
                    import_receipt_detail = ImportReceiptDetail(
                        medicine=medicine_instance,  # Now passing the Medicine instance
                        import_receipt=receipt,
                        quantity=quantity,
                        price=price,
                    )
                    import_receipt_detail.save()

                    updated_details.append(
                        {
                            "import_receipt": receipt.id,
                            "medicine": import_receipt_detail.medicine.id,
                            "quantity": import_receipt_detail.quantity,
                            "price": import_receipt_detail.price,
                        }
                    )

            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": updated_details,
                    "status": "success",
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )

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
        except Exception as e:
            return Response(
                {
                    "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": None,
                    "status": "error",
                    "errorMessage": f"Đã xảy ra lỗi: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
