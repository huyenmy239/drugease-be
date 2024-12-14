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


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['full_name', 'id_card', 'phone_number', 'email']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = Patient.objects.all()

        name = self.request.query_params.get('name', None)
        birth_year = self.request.query_params.get('birth_year', None)
        id_card = self.request.query_params.get('id_card', None)
        phone_number = self.request.query_params.get('phone_number', None)

        if name:
            queryset = queryset.filter(full_name__icontains=name)
        if birth_year:
            queryset = queryset.filter(date_of_birth__year=birth_year)
        if id_card:
            queryset = queryset.filter(id_card=id_card)
        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)

        return queryset
    
    def destroy(self, request, *args, **kwargs):
        patient = self.get_object()

        if patient.prescriptions.exists():
            raise ValidationError("Cannot delete patient because they have linked prescriptions.")

        return super().destroy(request, *args, **kwargs)
            

class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorListView(APIView):
    def get(self, request):
        doctors = Account.objects.filter(role='doctor').select_related('employee')
        data = [
            {
                "id": doctor.employee.id,
                "full_name": doctor.employee.full_name,
                "date_of_birth": doctor.employee.date_of_birth,
                "gender": doctor.employee.gender,
                "id_card": doctor.employee.id_card,
                "phone_number": doctor.employee.phone_number,
                "address": doctor.employee.address,
                "email": doctor.employee.email
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
                "employee_id": medicine.employee.id
            }
            for medicine in medicines
        ]
        return Response(data, status=status.HTTP_200_OK)


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor', None)
        
        if doctor_id is not None:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = serializer.save()

        details_data = request.data.get('details', [])
        for detail_data in details_data:
            detail_data['prescription'] = prescription.id
            detail_serializer = PrescriptionDetailSerializer(data=detail_data)
            detail_serializer.is_valid(raise_exception=True)
            detail_serializer.save()

        return Response(
            PrescriptionSerializer(prescription).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, 'export_receipts'):
            raise ValidationError("Cannot update a prescription that has an associated export receipt.")
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        prescription = serializer.save()

        details_data = request.data.get('details', [])
        existing_detail_ids = {detail.get('id') for detail in details_data if 'id' in detail}
        
        PrescriptionDetail.objects.filter(prescription=prescription).exclude(id__in=existing_detail_ids).delete()

        for detail_data in details_data:
            if 'id' in detail_data:
                detail_instance = PrescriptionDetail.objects.get(id=detail_data['id'], prescription=prescription)
                detail_serializer = PrescriptionDetailSerializer(detail_instance, data=detail_data, partial=partial)
                detail_serializer.is_valid(raise_exception=True)
                detail_serializer.save()
            else:
                detail_data['prescription'] = prescription.id
                detail_serializer = PrescriptionDetailSerializer(data=detail_data)
                detail_serializer.is_valid(raise_exception=True)
                detail_serializer.save()

        return Response(
            PrescriptionSerializer(prescription).data
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if hasattr(instance, 'export_receipts'):
            raise ValidationError("Cannot delete a prescription that has an associated export receipt.")

        return super().destroy(request, *args, **kwargs)
    


class PrescriptionListView(APIView):
    def get(self, request):
        doctor_id = request.query_params.get('doctor', None)

        if doctor_id:
            prescriptions = Prescription.objects.filter(doctor=doctor_id).order_by('-prescription_date')
        else:
            prescriptions = Prescription.objects.all().order_by('-prescription_date')
        serializer = PrescriptionViewSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)