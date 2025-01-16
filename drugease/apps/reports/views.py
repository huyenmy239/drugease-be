from datetime import datetime
from django.db.models import Sum, F
from jsonschema import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.prescriptions.models import Patient
from apps.warehouse.models import ImportReceipt, ImportReceiptDetail
from rest_framework import status
from rest_framework.views import APIView


class ReportPatient(APIView):
    def get(self, request):
        try:

            year = request.query_params.get('year', None)
            month = request.query_params.get('month', None)
            day = request.query_params.get('day', None)

            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)

            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

            if start_date and end_date:
                if end_date < start_date:
                    return Response({
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu."
                    }, status=status.HTTP_400_BAD_REQUEST)

                patients = Patient.objects.filter(registration_date__range=(start_date, end_date))

            elif day:
                patients = Patient.objects.filter(
                    registration_date__year=year,
                    registration_date__month=month,
                    registration_date__day=day
                )
            elif month:
                patients = Patient.objects.filter(registration_date__year=year, registration_date__month=month)
            elif year:
                patients = Patient.objects.filter(registration_date__year=year)
            else:
                patients = Patient.objects.all()

            male_count = patients.filter(gender=True).count()
            female_count = patients.filter(gender=False).count()
            total = male_count + female_count

            if start_date and end_date:
                time_period = f"Từ {start_date.strftime('%d/%m/%Y')} đến {end_date.strftime('%d/%m/%Y')}"
            else:
                time_period = f"{day}/{month}/{year}" if day else f"{month}/{year}" if month else f"{year}"

            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": {
                    "Thời gian": time_period,
                    "Nam": male_count,
                    "Nữ": female_count,
                    "Tổng": total
                },
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "status": "error",
                "errorMessage": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportMedicineCost(APIView):
    def get(self, request):
        try:
            # Lấy tham số từ query
            day = request.query_params.get('day', None)
            month = request.query_params.get('month', None)
            year = request.query_params.get('year', None)
            medicine_name = request.query_params.get('medicine_name', None)
            
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)

            # Kiểm tra nếu có start_date và end_date thì ngày kết thúc phải lớn hơn ngày bắt đầu
            if start_date and end_date:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                
                if end_date_obj < start_date_obj:
                    raise ValidationError("Ngày kết thúc phải lớn hơn ngày bắt đầu")

            filter_params = {}

            # Lọc theo start_date và end_date nếu có
            if start_date:
                filter_params['import_date__gte'] = start_date  # Lọc từ ngày bắt đầu
            if end_date:
                filter_params['import_date__lte'] = end_date  # Lọc đến ngày kết thúc
            
            # Nếu không có start_date và end_date, lọc theo năm, tháng, ngày
            if year:
                filter_params['import_date__year'] = year
            if month:
                filter_params['import_date__month'] = month
            if day:
                filter_params['import_date__day'] = day

            # Lọc phiếu nhập thuốc theo các tham số
            import_receipts = ImportReceipt.objects.filter(**filter_params)

            # Tính tổng chi phí cho từng loại thuốc
            details = ImportReceiptDetail.objects.filter(import_receipt__in=import_receipts).values(
                'medicine__medicine_name'
            ).annotate(
                total_cost=Sum(F('quantity') * F('price'))  # Tính tổng chi phí đúng cách
            )

            # Nếu có yêu cầu lọc theo tên thuốc
            if medicine_name:
                details = details.filter(medicine__medicine_name__icontains=medicine_name)

            # Chuyển đổi kết quả và thêm trường "Thời gian"
            result = []
            for detail in details:
                time_period = f"{month}.{year}" if month else f"{year}"
                result.append({
                    "Thời gian": time_period,
                    "medicine_name": detail['medicine__medicine_name'],
                    "total_cost": detail['total_cost']
                })

            # Trả về kết quả dưới dạng JSON theo yêu cầu
            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": result,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Trường hợp lỗi (VD: Ngày kết thúc nhỏ hơn ngày bắt đầu)
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Các lỗi khác
            return Response({
                "statuscode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "status": "error",
                "errorMessage": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)