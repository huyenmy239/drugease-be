import datetime
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import filters
from django.db.models import Q
from .models import Patient, Prescription, PrescriptionDetail
from .serializers import *
from apps.accounts.models import Account
from apps.warehouse.models import Medicine
from rest_framework.decorators import action
from django.db.models import Q

# class PatientViewSet(viewsets.ModelViewSet):
#     queryset = Patient.objects.all()
#     serializer_class = PatientSerializer
#     # permission_classes = [IsAuthenticated]
#     filter_backends = (filters.OrderingFilter, filters.SearchFilter)
#     search_fields = ['full_name', 'id_card', 'phone_number', 'email']
#     ordering_fields = '__all__'

#     def get_queryset(self):
#         queryset = Patient.objects.all()

#         name = self.request.query_params.get('name', None)
#         birth_year = self.request.query_params.get('birth_year', None)
#         id_card = self.request.query_params.get('id_card', None)
#         phone_number = self.request.query_params.get('phone_number', None)

#         if name:
#             queryset = queryset.filter(full_name__icontains=name)
#         if birth_year:
#             queryset = queryset.filter(date_of_birth__year=birth_year)
#         if id_card:
#             queryset = queryset.filter(id_card=id_card)
#         if phone_number:
#             queryset = queryset.filter(phone_number=phone_number)

#         return queryset

#     def destroy(self, request, *args, **kwargs):
#         patient = self.get_object()

#         if patient.prescriptions.exists():
#             raise ValidationError("Cannot delete patient because they have linked prescriptions.")

#         return super().destroy(request, *args, **kwargs)


class PatientListView(APIView):

    def get(self, request):
        # Lấy tất cả bệnh nhân
        patients = Patient.objects.all()

        # Lặp qua tất cả bệnh nhân và thêm thông tin nhân viên
        patient_data = []
        for patient in patients:
            # Lấy dữ liệu bệnh nhân qua serializer
            serialized_patient = PatientSerializer(patient).data

            # Thêm thông tin nhân viên vào dữ liệu của bệnh nhân
            serialized_patient["employee"] = (
                patient.employee.full_name if patient.employee else None
            )

            # Thêm vào danh sách kết quả
            patient_data.append(serialized_patient)

        return Response(
            {
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": patient_data,  # Trả về dữ liệu đã được thêm thông tin nhân viên
                "errorMessage": None,
            },
            status=status.HTTP_200_OK,
        )


class PatientDetailView(APIView):
    """
    API để lấy chi tiết bệnh nhân theo ID.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            # Lấy bệnh nhân theo ID
            patient = Patient.objects.get(pk=pk)

            # Serializer cho bệnh nhân
            serializer = PatientSerializer(patient)

            # Thêm thông tin nhân viên (nếu có)
            data = serializer.data
            data["employee"] = patient.employee.full_name if patient.employee else None

            return Response(
                {
                    "statusCode": status.HTTP_200_OK,
                    "status": "success",
                    "data": data,
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )
        except Patient.DoesNotExist:
            # Trả về lỗi nếu không tìm thấy bệnh nhân
            return Response(
                {
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "status": "error",
                    "data": None,
                    "errorMessage": "Patient not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    # Tìm kiếm bệnh nhân (theo tên, số điện thoại, hoặc email)
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        full_name = request.query_params.get("full_name", None)
        phone_number = request.query_params.get("phone_number", None)
        email = request.query_params.get("email", None)

        filters = Q()
        if full_name:
            filters &= Q(full_name__icontains=full_name)
        if phone_number:
            filters &= Q(phone_number__icontains=phone_number)
        if email:
            filters &= Q(email__icontains=email)

        patients = Patient.objects.filter(filters)
        serializer = PatientSerializer(patients, many=True)
        return Response(
            {
                "statusCode": 200,
                "status": "success",
                "data": serializer.data,
                "errorMessage": None,
            }
        )

    # Tùy chỉnh phương thức tạo (POST)
    def create(self, request, *args, **kwargs):
        """
        Thêm bệnh nhân mới.
        """
        serializer = self.get_serializer(data=request.data)
        print("request.data", request.data)
        if serializer.is_valid():
            serializer.save()
            patient = Patient.objects.get(id=serializer.data["id"]).employee.full_name
            print("patient", patient)
            return Response(
                {
                    "statusCode": status.HTTP_201_CREATED,
                    "status": "success",
                    "data": serializer.data,
                    "errorMessage": None,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "status": "error",
                    "errorMessage": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Tùy chỉnh phương thức cập nhật (PUT/PATCH)
    def update(self, request, *args, **kwargs):
        """
        Cập nhật các trường phone_number, address, email, insurance của bệnh nhân.
        """
        # Lấy bệnh nhân từ DB
        instance = self.get_object()

        # Lọc các trường cần cập nhật
        update_data = {}
        allowed_fields = ["phone_number", "address", "email", "insurance"]
        for field in allowed_fields:
            if field in request.data:
                update_data[field] = request.data[field]

        # Sử dụng serializer để validate và cập nhật dữ liệu
        serializer = PatientSerializer(instance, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "statusCode": status.HTTP_200_OK,
                    "status": "success",
                    "data": serializer.data,
                    "errorMessage": None,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "status": "error",
                    "errorMessage": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Tùy chỉnh phương thức xóa (DELETE)
    def destroy(self, request, *args, **kwargs):
        """
        Xóa bệnh nhân theo ID, kiểm tra nếu bệnh nhân đã có đơn thuốc trước khi xóa.
        """
        patient = self.get_object()

        # Kiểm tra nếu bệnh nhân có liên kết với đơn thuốc
        if Prescription.objects.filter(patient=patient).exists():
            return Response(
                {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "status": "error",
                    "errorMessage": "Không thể xóa bệnh nhân đã có đơn thuốc.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Nếu không có đơn thuốc, tiến hành xóa bệnh nhân
        patient.delete()
        return Response(
            {
                "statusCode": status.HTTP_204_NO_CONTENT,
                "status": "success",
                "data": None,
                "errorMessage": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class DoctorListView(APIView):
    def get(self, request):
        doctors = Account.objects.filter(role="doctor").select_related("employee")
        data = [
            {
                "id": doctor.employee.id,
                "full_name": doctor.employee.full_name,
                "date_of_birth": doctor.employee.date_of_birth,
                "gender": doctor.employee.gender,
                "id_card": doctor.employee.id_card,
                "phone_number": doctor.employee.phone_number,
                "address": doctor.employee.address,
                "email": doctor.employee.email,
            }
            for doctor in doctors
        ]
        return Response(data, status=status.HTTP_200_OK)


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
        return Response(data, status=status.HTTP_200_OK)


# class PrescriptionViewSet(viewsets.ModelViewSet):
#     queryset = Prescription.objects.all()
#     serializer_class = PrescriptionSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         doctor_id = self.request.query_params.get("doctor", None)

#         if doctor_id is not None:
#             queryset = queryset.filter(doctor_id=doctor_id)

#         return queryset

#     def retrieve(self, request, *args, **kwargs):
#         prescription = self.get_object()

#         # Serializing Prescription (tùy vào bạn muốn kiểu dữ liệu nào)
#         serializer = PrescriptionViewSerializer(prescription)

#         # Trả về dữ liệu Prescription dưới dạng JSON
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         prescription = serializer.save()

#         details_data = request.data.get("details", [])

#         for detail_data in details_data:
#             detail_data["prescription"] = prescription.id
#             detail_serializer = PrescriptionDetailSerializer(data=detail_data)
#             detail_serializer.is_valid(raise_exception=True)
#             detail_serializer.save()

#         return Response(
#             PrescriptionSerializer(prescription).data, status=status.HTTP_201_CREATED
#         )

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if hasattr(instance, "export_receipts"):
#             raise ValidationError(
#                 "Cannot update a prescription that has an associated export receipt."
#             )

#         partial = kwargs.pop("partial", False)
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         prescription = serializer.save()

#         details_data = request.data.get("details", [])
#         existing_detail_ids = {
#             detail.get("id") for detail in details_data if "id" in detail
#         }

#         PrescriptionDetail.objects.filter(prescription=prescription).exclude(
#             id__in=existing_detail_ids
#         ).delete()

#         for detail_data in details_data:
#             if "id" in detail_data:
#                 detail_instance = PrescriptionDetail.objects.get(
#                     id=detail_data["id"], prescription=prescription
#                 )
#                 detail_serializer = PrescriptionDetailSerializer(
#                     detail_instance, data=detail_data, partial=partial
#                 )
#                 detail_serializer.is_valid(raise_exception=True)
#                 detail_serializer.save()
#             else:
#                 detail_data["prescription"] = prescription.id
#                 detail_serializer = PrescriptionDetailSerializer(data=detail_data)
#                 detail_serializer.is_valid(raise_exception=True)
#                 detail_serializer.save()

#         return Response(PrescriptionSerializer(prescription).data)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()

#         if hasattr(instance, "export_receipts"):
#             raise ValidationError(
#                 "Cannot delete a prescription that has an associated export receipt."
#             )

#         return super().destroy(request, *args, **kwargs)


# class PrescriptionListView(APIView):

    # def get(self, request):
    #     doctor_id = request.query_params.get("doctor", None)

    #     if doctor_id:
    #         prescriptions = Prescription.objects.filter(doctor=doctor_id).order_by(
    #             "-prescription_date"
    #         )
    #     else:
    #         prescriptions = Prescription.objects.all().order_by("-prescription_date")
    #     serializer = PrescriptionViewSerializer(prescriptions, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    def get_serializer_class(self):
        # Nếu là phương thức POST (create), sử dụng serializer tạo mới
        if self.action == 'create':
            return PrescriptionCreateSerializer
        # Nếu không phải là POST (get, update, delete), sử dụng serializer xem
        return PrescriptionViewSerializer

    #Lọc theo mã bác sĩ
    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get("doctor", None)

        if doctor_id is not None:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

    #Tìm kiếm theo đơn thuốc
    def retrieve(self, request, *args, **kwargs):
        prescription = self.get_object()

        # Serialize Prescription
        serializer = PrescriptionViewSerializer(prescription)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = PrescriptionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = serializer.save()

        patient_id = request.data.get("patient")
        doctor_id = request.data.get("doctor")

        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            result = {
                "statuscode": status.HTTP_404_NOT_FOUND,
                "data": None,
                "status": "error",
                "errorMessage": "Patient with this ID does not exist."
            }
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        try:
            doctor = Employee.objects.get(id=doctor_id)
        except Employee.DoesNotExist:
            result = {
                "statuscode": status.HTTP_404_NOT_FOUND,
                "data": None,
                "status": "error",
                "errorMessage": "Doctor with this ID does not exist."
            }
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        prescription.patient = patient
        prescription.doctor = doctor
        prescription.save()

        details_data = request.data.get("details", [])

        for detail_data in details_data:
            medicine_id = detail_data.get("medicine")  
            quantity = detail_data.get("quantity")

            try:
                medicine = Medicine.objects.get(id=medicine_id)
            except Medicine.DoesNotExist:
                result = {
                    "statuscode": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "status": "error",
                    "errorMessage": f"Medicine with ID {medicine_id} not found."
                }
                return Response(result, status=status.HTTP_404_NOT_FOUND)

            if quantity > medicine.stock_quantity:
                result = {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": f"Not enough stock for medicine {medicine_id}. Available stock is {medicine.stock_quantity}."
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            medicine.stock_quantity -= quantity
            medicine.save()

            detail_data["prescription"] = prescription.id
            detail_serializer = PrescriptionDetailSerializer(data=detail_data)

            if not detail_serializer.is_valid():
                result = {
                    "statuscode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": detail_serializer.errors
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            detail_serializer.save()

        result = {
            "statuscode": status.HTTP_201_CREATED,
            "data": PrescriptionViewSerializer(prescription).data,
            "status": "success",
            "errorMessage": None
        }

        return Response(result, status=status.HTTP_201_CREATED)



    def update(self, request, *args, **kwargs):
        prescription_id = kwargs.get("pk")
        try:
            prescription = Prescription.objects.get(id=prescription_id)
        except Prescription.DoesNotExist:
            result = {
                "statuscode": status.HTTP_404_NOT_FOUND,
                "data": None,
                "status": "error",
                "errorMessage": f"Prescription with ID {prescription_id} does not exist."
            }
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        if hasattr(prescription, "export_receipts"):
            result = {
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": "Cannot update a prescription that has an associated export receipt."
            }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        prescription.diagnosis = request.data.get("diagnosis", prescription.diagnosis)
        prescription.patient = request.data.get("patient", prescription.patient)
        prescription.doctor = request.data.get("doctor", prescription.doctor)
        prescription.save()

        details_data = request.data.get("details", None)

        if details_data is not None: 
            old_details = PrescriptionDetail.objects.filter(prescription=prescription)

            old_details.delete()

            for detail_data in details_data:
                medicine_id = detail_data.get("medicine")  
                quantity = detail_data.get("quantity")

                try:
                    medicine = Medicine.objects.get(id=medicine_id)
                except Medicine.DoesNotExist:
                    result = {
                        "statuscode": status.HTTP_404_NOT_FOUND,
                        "data": None,
                        "status": "error",
                        "errorMessage": f"Medicine with ID {medicine_id} not found."
                    }
                    return Response(result, status=status.HTTP_404_NOT_FOUND)

                if quantity > medicine.stock_quantity:
                    result = {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": f"Not enough stock for medicine {medicine_id}. Available stock is {medicine.stock_quantity}."
                    }
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)

                if old_details.exists():
                    old_quantity = old_details.get(medicine_id=medicine_id).quantity
                    if quantity < old_quantity:
                        medicine.stock_quantity += (old_quantity - quantity)
                    else:  
                        medicine.stock_quantity = medicine.stock_quantity + old_quantity - quantity
                else:
                    medicine.stock_quantity -= quantity

                medicine.save()

                detail_data["prescription"] = prescription.id
                detail_serializer = PrescriptionDetailSerializer(data=detail_data)
                if not detail_serializer.is_valid():
                    result = {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": detail_serializer.errors
                    }
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                detail_serializer.save()

        result = {
            "statuscode": status.HTTP_200_OK,
            "data": PrescriptionViewSerializer(prescription).data,
            "status": "success",
            "errorMessage": None
        }

        return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if hasattr(instance, "export_receipts"):
            raise ValidationError("Cannot delete a prescription that has an associated export receipt.")

        return super().destroy(request, *args, **kwargs)