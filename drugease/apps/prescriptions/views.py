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
<<<<<<< HEAD
from django.shortcuts import get_object_or_404
=======

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
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

>>>>>>> 221eb584e957ca1f61a11301cdea0185cb16971d

class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet quản lý bệnh nhân.
    """
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def list(self, request):
        """
        Lấy danh sách bệnh nhân.
        """
        patients = Patient.objects.all()

        # Sử dụng PatientSerializer để serialize dữ liệu
        serializer = PatientSerializer(patients, many=True)

        return Response({
            "statuscode": status.HTTP_200_OK,
            "data": serializer.data,
            "status": "success",
            "errorMessage": None,
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        full_name = request.query_params.get("full_name", "")
        phone_number = request.query_params.get("phone_number", "")
        email = request.query_params.get("email", "")

        patients = Patient.objects.filter(
            full_name__icontains=full_name,
            phone_number__icontains=phone_number,
            email__icontains=email,
        )
        serializer = PatientSerializer(patients, many=True)
        return Response(
            {
                "statusCode": status.HTTP_200_OK,
                "status": "success",
                "data": serializer.data,
                "errorMessage": None,
            }
        )

    def create(self, request, *args, **kwargs):
        """
        Thêm bệnh nhân mới.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "statusCode": status.HTTP_201_CREATED,
                    "status": "success",
                    "data": serializer.data,
                    "errorMessage": None,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "status": "error",
                "errorMessage": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        """
        Cập nhật các trường phone_number, address, email, insurance của bệnh nhân.
        """
        instance = self.get_object()

        # Chỉ cập nhật các trường cần thiết
        update_data = {}
        for field in ["phone_number", "address", "email", "insurance"]:
            if field in request.data:
                update_data[field] = request.data[field]

        if not update_data:
            return Response(
                {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "status": "error",
                    "errorMessage": "Chỉ được cập nhật số điện thoại, địa chỉ, email và bảo hiểm.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sử dụng serializer với partial = True để cập nhật một số trường
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
        return Response(
            {
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "status": "error",
                "errorMessage": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Xóa bệnh nhân.
        """
        instance = self.get_object()

        if Prescription.objects.filter(patient=instance).exists():
            return Response(
                {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "status": "error",
                    "data": None,
                    "errorMessage": "Bệnh nhân không thể xóa vì có liên kết với phiếu xuất.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
<<<<<<< HEAD
=======

>>>>>>> 221eb584e957ca1f61a11301cdea0185cb16971d

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
            }
            for medicine in medicines
        ]
        return Response(data, status=status.HTTP_200_OK)

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