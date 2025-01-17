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
from django.shortcuts import get_object_or_404

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
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDetailView(APIView):
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
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


class DoctorListView(APIView):
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get("doctor", None)

        if doctor_id is not None:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = serializer.save()

        details_data = request.data.get("details", [])
        for detail_data in details_data:
            detail_data["prescription"] = prescription.id
            detail_serializer = PrescriptionDetailSerializer(data=detail_data)
            detail_serializer.is_valid(raise_exception=True)
            detail_serializer.save()

        return Response(
            PrescriptionSerializer(prescription).data, status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, "export_receipts"):
            raise ValidationError(
                "Cannot update a prescription that has an associated export receipt."
            )

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        prescription = serializer.save()

        details_data = request.data.get("details", [])
        existing_detail_ids = {
            detail.get("id") for detail in details_data if "id" in detail
        }

        PrescriptionDetail.objects.filter(prescription=prescription).exclude(
            id__in=existing_detail_ids
        ).delete()

        for detail_data in details_data:
            if "id" in detail_data:
                detail_instance = PrescriptionDetail.objects.get(
                    id=detail_data["id"], prescription=prescription
                )
                detail_serializer = PrescriptionDetailSerializer(
                    detail_instance, data=detail_data, partial=partial
                )
                detail_serializer.is_valid(raise_exception=True)
                detail_serializer.save()
            else:
                detail_data["prescription"] = prescription.id
                detail_serializer = PrescriptionDetailSerializer(data=detail_data)
                detail_serializer.is_valid(raise_exception=True)
                detail_serializer.save()

        return Response(PrescriptionSerializer(prescription).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if hasattr(instance, "export_receipts"):
            raise ValidationError(
                "Cannot delete a prescription that has an associated export receipt."
            )

        return super().destroy(request, *args, **kwargs)


class PrescriptionListView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        doctor_id = request.query_params.get("doctor", None)

        if doctor_id:
            prescriptions = Prescription.objects.filter(doctor=doctor_id).order_by(
                "-prescription_date"
            )
        else:
            prescriptions = Prescription.objects.all().order_by("-prescription_date")
        serializer = PrescriptionViewSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

