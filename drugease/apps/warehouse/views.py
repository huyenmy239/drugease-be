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
from django.db.models import F, Sum
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import re



# view for Medicine
# @permission_classes([IsAuthenticated])
# class MedicineListView(APIView):
#     def get(self, request):
#         medicines = Medicine.objects.all()

#         # In ra toàn bộ danh sách thuốc
#         print("Medicines fetched from DB:", medicines)

#         data = []
#         for medicine in medicines:
#             print(
#                 f"Processing medicine: {medicine.medicine_name}"
#             )  # In ra tên thuốc trước khi xử lý

#             # Kiểm tra xem thuốc có hình ảnh hay không
#             if medicine.image:
#                 try:
#                     print(f"Medicine {medicine.medicine_name} has an image.")
#                     img = Image.open(medicine.image.path)
#                     buffered = BytesIO()
#                     img.save(buffered, format="PNG")
#                     img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
#                     image_data = f"data:image/png;base64,{img_str}"
#                 except Exception as e:
#                     print(f"Error converting image to base64: {e}")
#                     image_data = None
#             else:
#                 print(f"Medicine {medicine.medicine_name} does not have an image.")
#                 image_data = None

#             # Thêm thông tin thuốc vào danh sách
#             data.append(
#                 {
#                     "id": medicine.id,
#                     "medicine_name": medicine.medicine_name,
#                     "unit": medicine.unit,
#                     "sale_price": medicine.sale_price,
#                     "description": medicine.description,
#                     "stock_quantity": medicine.stock_quantity,
#                     "image": image_data,
#                 }
#             )

#         # In ra kết quả trước khi trả về Response
#         print("Final data to be returned:", data)

#         return Response(
#             {
#                 "statuscode": status.HTTP_200_OK,
#                 "data": data,
#                 "status": "success",
#                 "errorMessage": None,
#             },
#             status=status.HTTP_200_OK,
#         )


#     def get(self, request, pk):
#         try:
#             # Lấy chi tiết kho theo ID (pk)
#             warehouse = Warehouse.objects.get(pk=pk)
#             serializer = WarehouseSerializer(warehouse)

#             # Tạo response JSON
#             response = {
#                 "statusCode": status.HTTP_200_OK,
#                 "status": "success",
#                 "data": serializer.data,
#                 "errorMessage": None,
#             }
#             return Response(response, status=status.HTTP_200_OK)

#         except Warehouse.DoesNotExist:
#             # Trả về lỗi nếu kho không tồn tại
#             response = {
#                 "statusCode": status.HTTP_404_NOT_FOUND,
#                 "status": "error",
#                 "data": None,
#                 "errorMessage": "Warehouse not found.",
#             }
#             return Response(response, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             # Trả về lỗi cho các trường hợp ngoại lệ khác
#             response = {
#                 "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 "status": "error",
#                 "data": None,
#                 "errorMessage": str(e),
#             }
#             return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class MedicineViewSet(viewsets.ModelViewSet):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)

#             medicine_name = request.data.get("medicine_name")
#             unit = request.data.get("unit")
#             sale_price = request.data.get("sale_price")
#             total_amount = request.data.get("stock_quantity")
#             print("request.data", request.data)
#             if not medicine_name.strip():
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Không được bỏ trống tên thuốc.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             if not unit.strip():
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Không được bỏ trống đơn vị tính.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if int(sale_price) <= 0:
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Giá thuốc phải lớn hơn 0.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             print("total_amount", type(total_amount))
#             if int(total_amount) <= 0:
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Số lượng tồn phải lớn hơn 0.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             if Medicine.objects.filter(medicine_name=medicine_name).exists():
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Tên thuốc này đã tồn tại.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if serializer.is_valid():
#                 serializer.save()
#                 print("serializer.data", serializer.data)
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_201_CREATED,
#                         "data": serializer.data,
#                         "status": "success",
#                         "errorMessage": None,
#                     },
#                     status=status.HTTP_201_CREATED,
#                 )
#             else:
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": serializer.errors,
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except Exception as e:
#             return Response(
#                 {
#                     "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     "data": None,
#                     "status": "error",
#                     "errorMessage": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


#     def update(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()

#             serializer = self.get_serializer(instance, data=request.data)

#             unit = request.data.get("unit", "")
#             sale_price = request.data.get("sale_price", 0)
#             print("request", request.data)
#             if not unit.strip():
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Không được bỏ trống đơn vị tính.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if sale_price <= 0:
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Giá thuốc phải lớn hơn 0.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if serializer.is_valid():

#                 serializer.save()
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_200_OK,
#                         "data": serializer.data,
#                         "status": "success",
#                         "errorMessage": None,
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": serializer.errors,
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except Exception as e:
#             return Response(
#                 {
#                     "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     "data": None,
#                     "status": "error",
#                     "errorMessage": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     def destroy(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()

#             if ImportReceiptDetail.objects.filter(medicine=instance).exists():
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Thuốc này không thể xóa vì đã tồn tại trong phiếu nhập.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if PrescriptionDetail.objects.filter(medicine=instance).exists():
#                 return Response(
#                     {
#                         "statuscode": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "status": "error",
#                         "errorMessage": "Thuốc này không thể xóa vì đã tồn tại trong phiếu xuất.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             instance.delete()
#             return Response(
#                 {
#                     "statuscode": status.HTTP_204_NO_CONTENT,
#                     "data": None,
#                     "status": "success",
#                     "errorMessage": None,
#                 },
#                 status=status.HTTP_204_NO_CONTENT,
#             )


#         except Exception as e:
#             return Response(
#                 {
#                     "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     "data": None,
#                     "status": "error",
#                     "errorMessage": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#View for Medicine
# @permission_classes([IsAuthenticated])
class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    # parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        medicines = Medicine.objects.all()
        data = [self._serialize_medicine(medicine) for medicine in medicines]
        return Response({
            "statuscode": status.HTTP_200_OK,
            "data": data,
            "status": "success",
            "errorMessage": None,
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            medicine = self.get_object()
            serializer = self.get_serializer(medicine)
            return Response({
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": serializer.data,
                "errorMessage": None,
            }, status=status.HTTP_200_OK)
        except Medicine.DoesNotExist:
            return self._error_response(status.HTTP_404_NOT_FOUND, "Medicine not found.")
        except Exception as e:
            return self._error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            medicines = Medicine.objects.filter(medicine_name__icontains=query)
            data = [self._serialize_medicine(medicine) for medicine in medicines]
            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": data,
                "status": "success",
                "errorMessage": None,
            }, status=status.HTTP_200_OK)
        else:
            return self._error_response(status.HTTP_400_BAD_REQUEST, "Query parameter 'q' is required.")

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()

            # Lấy serializer với dữ liệu đã được cập nhật
            serializer = self.get_serializer(data=data)

            # Validate dữ liệu
            self._validate_medicine_data(data)

            # Kiểm tra xem tên thuốc đã tồn tại hay chưa
            if Medicine.objects.filter(medicine_name=data.get("medicine_name")).exists():
                return self._error_response(status.HTTP_400_BAD_REQUEST, "Tên thuốc đã tồn tại.")

            # Kiểm tra tính hợp lệ của dữ liệu qua serializer
            if serializer.is_valid():
                serializer.save()  # Lưu đối tượng thuốc mới
                return Response({
                    "statuscode": status.HTTP_201_CREATED,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                }, status=status.HTTP_201_CREATED)
            else:
                return self._error_response(status.HTTP_400_BAD_REQUEST, serializer.errors)
        except ValueError as e:
            return self._error_response(status.HTTP_400_BAD_REQUEST, str(e))
        except Exception as e:
            return self._error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def update(self, request, *args, **kwargs):
        try:
            # Lấy đối tượng cần cập nhật
            instance = self.get_object()

            serializer = self.get_serializer(instance, data=request.data)


            if serializer.is_valid():
                serializer.save()
                return Response({
                    "statuscode": status.HTTP_200_OK,
                    "data": serializer.data,
                    "status": "success",
                    "errorMessage": None,
                }, status=status.HTTP_200_OK)
            else:
                return self._error_response(status.HTTP_400_BAD_REQUEST, serializer.errors)
        except Exception as e:
            return self._error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if ImportReceiptDetail.objects.filter(medicine=instance).exists() or PrescriptionDetail.objects.filter(medicine=instance).exists():
                return self._error_response(status.HTTP_400_BAD_REQUEST, "Thuốc đã tồn tại trong phiếu nhập (hoặc xuất).")

            instance.delete()
            
            return Response({
                "statuscode": status.HTTP_204_NO_CONTENT,
                "data": None,
                "status": "success",
                "errorMessage": None,
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return self._error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _serialize_medicine(self, medicine):
        return {
            "id": medicine.id,
            "medicine_name": medicine.medicine_name,
            "unit": medicine.unit,
            "sale_price": medicine.sale_price,
            "description": medicine.description,
            "stock_quantity": medicine.stock_quantity,
        }

    def _validate_medicine_data(self, data):
        if not data.get("medicine_name", "").strip():
            raise ValueError("Medicine name cannot be empty.")
        unit = data.get("unit", "").strip()
    
        if not unit:
            raise ValueError("Unit cannot be empty.")
        
        # Kiểm tra unit với tiếng việt hợp lệ
        if not re.match(r"^[\w\sàáảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]+$", unit):
            raise ValueError("Unit must not contain numbers or special characters.")

        if int(data.get("sale_price", 0)) <= 0:
            raise ValueError("Sale price must be greater than 0.")
        if int(data.get("stock_quantity", 0)) <= 0:
            raise ValueError("Stock quantity must be greater than 0.")

    def _error_response(self, status_code, error_message):
        return Response({
            "statuscode": status_code,
            "data": None,
            "status": "error",
            "errorMessage": error_message,
        }, status=status_code)

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

    # def get_queryset(self):
    #     """
    #     Override this method to add search functionality.
    #     """
    #     queryset = Warehouse.objects.all()
    #     search_query = self.request.query_params.get("q", None)
    #     if search_query:
    #         queryset = queryset.filter(warehouse_name__icontains=search_query)
    #     return queryset
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Tìm kiếm kho theo địa chỉ và trạng thái is_active.
        """
        # Lấy các tham số từ query params
        address = request.query_params.get("address", None)
        is_active = request.query_params.get("is_active", None)

        # Lọc dữ liệu
        warehouses = Warehouse.objects.all()
        if address:
            warehouses = warehouses.filter(address__icontains=address)
        if is_active is not None:
            warehouses = warehouses.filter(is_active=is_active.lower() == "true")

        # Serialize dữ liệu
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(
            {
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": serializer.data,
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle custom validation if needed.
        """
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
        # Lấy đối tượng cần cập nhật
        instance = self.get_object()

        # Lấy dữ liệu từ request
        address = request.data.get("address")
        is_active = bool(request.data.get("is_active"))
        print("is_active bool", is_active)

        check_response = check_not_empty(address, "địa chỉ kho")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        # Lọc các trường cần cập nhật
        update_data = {}
        if address:
            update_data["address"] = address
        if is_active is not None:  # Nếu is_active có trong request thì cập nhật
            update_data["is_active"] = is_active

        # Sử dụng serializer để validate và cập nhật dữ liệu
        serializer = self.get_serializer(instance, data=update_data, partial=True)
        if serializer.is_valid():
            # Lưu và trả về phản hồi thành công
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


class ImportReceiptCreateView(APIView):
    serializer_class = ImportReceiptAndDetailSerializer

    def post(self, request, *args, **kwargs):
        """
        Xử lý yêu cầu POST để tạo phiếu nhập và chi tiết phiếu nhập,
        đồng thời cập nhật total_amount cho phiếu nhập.
        """
        # Khởi tạo serializer với dữ liệu từ request
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():  # Đảm bảo mọi thao tác đều thành công trong một giao dịch
                    import_receipt = (
                        serializer.save()
                    )  # Tạo phiếu nhập và chi tiết phiếu nhập

                    # Tính toán total_amount từ các chi tiết
                    total_amount = 0
                    for detail in import_receipt.details.all():
                        total_amount += detail.quantity * detail.price

                    # Cập nhật total_amount cho phiếu nhập
                    import_receipt.total_amount = total_amount
                    import_receipt.save()
                    serializer.update_stock_quantity(import_receipt)
                    # Trả về phản hồi thành công
                    return Response(
                        {
                            "statusCode": status.HTTP_201_CREATED,
                            "status": "success",
                            "data": serializer.data,
                            "errorMessage": None,
                        },
                        status=status.HTTP_201_CREATED,
                    )
            except Exception as e:
                return Response(
                    {
                        "statusCode": status.HTTP_400_BAD_REQUEST,
                        "status": "error",
                        "data": None,
                        "errorMessage": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "status": "error",
                    "data": None,
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
        Tạo mới ImportReceipt.
        Nếu is_approved được duyệt, cập nhật quantity của các Medicine liên quan.
        """
        warehouse = request.data.get("warehouse")
        import_date = request.data.get("import_date")
        is_approved = bool(request.data.get("is_approved"))
        employee = request.data.get("employee")

        # Kiểm tra các trường không trống
        check_response = check_not_empty(warehouse, "Kho")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        check_response = check_not_empty(employee, "Nhân viên")
        if check_response:
            return check_response  # Trả về lỗi nếu không hợp lệ

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Bắt đầu transaction
                with transaction.atomic():
                    # Lưu phiếu nhập
                    import_receipt = serializer.save()

                    # Nếu phiếu nhập được phê duyệt, cập nhật số lượng thuốc
                    if is_approved:
                        details = ImportReceiptDetail.objects.filter(
                            detail=import_receipt
                        )
                        for detail in details:
                            medicine = detail.medicine
                            medicine.quantity += detail.quantity
                            medicine.save()  # Nếu không có lỗi sẽ commit toàn bộ

                return Response(
                    {
                        "statuscode": status.HTTP_201_CREATED,
                        "data": serializer.data,
                        "status": "success",
                        "errorMessage": None,
                    },
                    status=status.HTTP_201_CREATED,
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
        Cập nhật ImportReceipt.
        Nếu is_approved được duyệt, cập nhật quantity của các Medicine liên quan.
        """
        instance = self.get_object()
        is_approved = bool(request.data.get("is_approved"))

        # Không cho phép sửa nếu phiếu nhập đã được phê duyệt trước đó
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

        # Kiểm tra nếu trạng thái chuyển từ False sang True
        if not instance.is_approved and is_approved:
            try:
                # Bắt đầu transaction
                with transaction.atomic():
                    details = ImportReceiptDetail.objects.filter(
                        import_receipt=instance
                    )
                    for detail in details:
                        medicine = detail.medicine
                        medicine.stock_quantity += detail.quantity
                        medicine.save()  # Nếu không có lỗi sẽ commit toàn bộ

                    # Cập nhật các trường khác
                    update_data = {
                        key: value
                        for key, value in request.data.items()
                        if value is not None
                    }
                    serializer = self.get_serializer(
                        instance, data=update_data, partial=True
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

        # Nếu không có thay đổi về is_approved, thực hiện cập nhật thông thường
        update_data = {
            key: value for key, value in request.data.items() if value is not None
        }
        serializer = self.get_serializer(instance, data=update_data, partial=True)
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


## hàm dùng để lấy chi tiết của một phiếu nhập
class ImportReceiptDetailsByIdAPIView(APIView):
    """
    API endpoint để xem tất cả chi tiết của các phiếu nhập hoặc chi tiết theo ID phiếu nhập.
    """

    def get(self, request, pk=None):
        try:
            if pk:
                # Lấy chi tiết cho phiếu nhập cụ thể
                details = ImportReceiptDetail.objects.filter(import_receipt=pk)
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
                    "medicine": detail.medicine.medicine_name,
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
        Đồng thời cập nhật lại total_amount của phiếu nhập.
        """
        print("request.data", request.data)
        try:
            receipt = ImportReceipt.objects.get(pk=pk)
            details = request.data.get("details", [])

            updated_details = []
            # Lấy tất cả các chi tiết phiếu nhập hiện có
            current_details = list(receipt.details.all())
            current_medicine_ids = [detail.medicine.id for detail in current_details]

            # Tạo danh sách medicine_id từ đầu vào
            input_medicine_ids = [detail.get("medicine") for detail in details]

            # Xóa các chi tiết không có trong đầu vào
            for current_detail in current_details:
                if current_detail.medicine.id not in input_medicine_ids:
                    current_detail.delete()

            # Cập nhật hoặc tạo mới chi tiết phiếu nhập
            for detail in details:
                medicine_id = detail.get("medicine")
                quantity = detail.get("quantity")
                price = detail.get("price")

                # Lấy đối tượng Medicine bằng medicine_id
                medicine_instance = Medicine.objects.get(id=medicine_id)

                try:
                    # Kiểm tra nếu đã tồn tại ImportReceiptDetail
                    import_receipt_detail = ImportReceiptDetail.objects.get(
                        medicine=medicine_instance, import_receipt=receipt
                    )
                    # Nếu có, cập nhật giá trị
                    import_receipt_detail.quantity = quantity
                    import_receipt_detail.price = price
                    import_receipt_detail.save()

                    updated_details.append(
                        {
                            "import_receipt": receipt.id,
                            "medicine": import_receipt_detail.medicine.medicine_name,
                            "quantity": import_receipt_detail.quantity,
                            "price": import_receipt_detail.price,
                        }
                    )

                except ImportReceiptDetail.DoesNotExist:
                    # Nếu không tồn tại, tạo mới chi tiết phiếu nhập
                    import_receipt_detail = ImportReceiptDetail(
                        medicine=medicine_instance,
                        import_receipt=receipt,
                        quantity=quantity,
                        price=price,
                    )
                    import_receipt_detail.save()

                    updated_details.append(
                        {
                            "import_receipt": receipt.id,
                            "medicine": import_receipt_detail.medicine.medicine_name,
                            "quantity": import_receipt_detail.quantity,
                            "price": import_receipt_detail.price,
                        }
                    )

            # Tính lại total_amount của phiếu nhập
            total_amount = 0
            for detail in receipt.details.all():
                total_amount += detail.quantity * detail.price

            # Cập nhật total_amount cho phiếu nhập
            receipt.total_amount = total_amount
            receipt.save()

            # Trả về tất cả chi tiết của phiếu nhập sau khi cập nhật
            all_details = [
                {
                    "medicine": detail.medicine.medicine_name,
                    "quantity": detail.quantity,
                    "price": detail.price,
                }
                for detail in receipt.details.all()
            ]

            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": {
                        "import_receipt": receipt.id,
                        "total_amount": receipt.total_amount,
                        "all_details": all_details,
                    },
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

    def _recalculate_total_amount(self, import_receipt):
        """
        Tính toán lại tổng số tiền (total_amount) của phiếu nhập dựa trên tất cả các chi tiết.
        """
        total_amount = sum(
            detail.quantity * detail.price
            for detail in ImportReceiptDetail.objects.filter(
                import_receipt=import_receipt
            )
        )
        import_receipt.total_amount = total_amount
        import_receipt.save()

    def create(self, request, *args, **kwargs):
        """
        Tạo mới ImportReceiptDetail và cập nhật total_amount của phiếu nhập.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Tạo ImportReceiptDetail
            import_receipt_detail = serializer.save()

            # Tính lại tổng số tiền
            self._recalculate_total_amount(import_receipt_detail.import_receipt)

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
        Cập nhật ImportReceiptDetail: chỉ cập nhật medicine, quantity và price.
        Giá (price) được lấy từ thuộc tính sale_price của thuốc.
        """
        instance = self.get_object()

        medicine_id = request.data.get("medicine")
        quantity = request.data.get("quantity")

        if not medicine_id:
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Thuốc không được để trống.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity is None:
            return Response(
                {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Số lượng không được để trống.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            medicine = Medicine.objects.get(id=medicine_id)
        except Medicine.DoesNotExist:
            return Response(
                {
                    "statuscode": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Thuốc không tồn tại.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.medicine = medicine
        instance.quantity = quantity
        instance.price = medicine.sale_price
        instance.save()

        self._recalculate_total_amount(instance.import_receipt)

        serializer = self.get_serializer(instance)
        return Response(
            {
                "statuscode": status.HTTP_200_OK,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Xóa ImportReceiptDetail và cập nhật total_amount của phiếu nhập.
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

        # Lưu tham chiếu đến phiếu nhập trước khi xóa
        import_receipt = instance.import_receipt

        # Xóa chi tiết phiếu nhập
        instance.delete()

        # Tính lại tổng số tiền
        self._recalculate_total_amount(import_receipt)

        return Response(
            {
                "statuscode": status.HTTP_204_NO_CONTENT,
                "data": None,
                "status": "success",
                "errorMessage": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )
