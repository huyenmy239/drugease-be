<<<<<<< HEAD
from datetime import datetime
from django.db.models import Sum, F
from jsonschema import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.prescriptions.models import Patient
from apps.warehouse.models import ImportReceipt, ImportReceiptDetail
from rest_framework import status
from rest_framework.views import APIView

=======
from django.db.models import Count, Min, Max, Sum, Avg, Q, F, ExpressionWrapper, DurationField, FloatField
from django.db.models.functions import TruncDate, TruncMonth
from django.utils.timezone import make_aware
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.prescriptions.models import Patient, Prescription, PrescriptionDetail
from apps.warehouse.models import *

from datetime import datetime

from jsonschema import ValidationError

class NumberofPrescriptionsPrescribedReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        prescriptions_data = (
            Prescription.objects.annotate(prescription_month=TruncMonth("prescription_date"))
            .values("doctor__full_name", "prescription_month")
            .annotate(
                total_prescriptions=Count("id"),
                unexported_prescriptions=Count("id", filter=Q(export_receipts=None)),
                exported_prescriptions=Count("id", filter=~Q(export_receipts=None)),
            )
            .order_by("prescription_month", "doctor__full_name")
        )

        report = []
        for data in prescriptions_data:
            report.append({
                "month": data["prescription_month"].strftime("%m/%Y"),
                "doctor": data["doctor__full_name"],
                "total_prescriptions": data["total_prescriptions"],
                "unexported_prescriptions": data["unexported_prescriptions"],
                "exported_prescriptions": data["exported_prescriptions"],
            })

        return Response(report)


class MedicationsinPrescriptionReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        medicine_data = (
            PrescriptionDetail.objects
            .values('medicine__medicine_name')
            .annotate(
                num_prescriptions=Count('prescription', distinct=True),
                total_quantity=Sum('quantity'),
                avg_quantity_per_prescription=Avg('quantity')
            )
        )

        report = [
            {
                "medicine_name": item['medicine__medicine_name'],
                "number_of_prescriptions": item['num_prescriptions'],
                "avg_per_prescription": round(item['avg_quantity_per_prescription'], 2),
                "total_quantity": item['total_quantity'],
            }
            for item in medicine_data
        ]

        return Response(report)
    

class MedicineExportReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = ExportReceiptDetail.objects.select_related(
            'export_receipt', 'medicine'
        ).filter(
            export_receipt__is_approved=True
        )

        report = queryset.annotate(
            month=TruncMonth('export_receipt__export_date')
        ).values(
            'month', 'medicine__medicine_name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by('month', '-total_quantity')

        data = []
        for entry in report:
            data.append({
                "time": entry['month'].strftime('%m/%Y') if entry['month'] else None,
                "medicine_name": entry['medicine__medicine_name'],
                "total_quantity": entry['total_quantity']
            })

        return Response(data)
    

class DoctorReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = Prescription.objects.filter(
            export_receipts__export_date__gte=F('prescription_date')
        ).select_related('doctor').annotate(
            doctor_name=F('doctor__full_name'),
            num_prescriptions=Count('id', distinct=True),
            avg_time=Avg(
                ExpressionWrapper(
                    F('export_receipts__export_date') - F('prescription_date'),
                    output_field=DurationField()
                )
            )
        ).values(
            'doctor_name',
            'num_prescriptions',
            'avg_time'
        )

        data = []
        for entry in queryset:
            avg_minutes = None
            if entry['avg_time']:
                avg_minutes = round(entry['avg_time'].total_seconds() / 60, 2)  # Chuyển đổi sang phút
            data.append({
                "doctor_name": entry['doctor_name'],
                "num_prescriptions": entry['num_prescriptions'],
                "avg_minutes": avg_minutes
            })

        return Response(data)
    

class PharmacistReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = ExportReceipt.objects.select_related('employee').filter(
            is_approved=True
        ).annotate(
            pharmacist_name=F('employee__full_name'),
            num_prescriptions=Count('id'),
            first_time=Min('export_date'),
            last_time=Max('export_date'),
            total_time=ExpressionWrapper(
                F('last_time') - F('first_time'),
                output_field=DurationField()
            )
        )

        data = []
        for entry in queryset:
            total_time_in_hours = None
            if entry.total_time:
                total_time_in_hours = entry.total_time.total_seconds() / 3600

            performance = None
            if total_time_in_hours and total_time_in_hours > 0:
                performance = round(entry.num_prescriptions / total_time_in_hours, 2)
            elif total_time_in_hours == None:
                performance = entry.num_prescriptions

            data.append({
                "pharmacist_name": entry.pharmacist_name,
                "num_prescriptions": entry.num_prescriptions,
                "performance": performance
            })

        return Response(data)
    

class MedicineRevenueReportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Truy vấn dữ liệu từ ExportReceiptDetail
        queryset = ExportReceiptDetail.objects.select_related(
            'export_receipt', 'medicine'
        ).filter(
            export_receipt__is_approved=True  # Chỉ lấy các phiếu xuất đã được duyệt
        ).annotate(
            month=TruncMonth('export_receipt__export_date'),  # Lấy tháng từ ngày xuất
            revenue=F('quantity') * F('price')  # Doanh thu = số lượng * giá
        ).values(
            'month', 'medicine__medicine_name'
        ).annotate(
            total_revenue=Sum('revenue', output_field=FloatField()),  # Tổng doanh thu theo thuốc và tháng
        ).order_by('month', 'medicine__medicine_name')

        # Tính toán chi phí và lợi nhuận theo từng tháng
        data = []
        for entry in queryset:
            month = entry['month']
            medicine_name = entry['medicine__medicine_name']

            # Lấy tổng chi phí nhập trong cùng tháng
            import_details = ImportReceiptDetail.objects.filter(
                import_receipt__import_date__month=month.month,
                import_receipt__import_date__year=month.year,
                medicine__medicine_name=medicine_name
            ).aggregate(
                total_cost=Sum(F('quantity') * F('price'), output_field=FloatField())
            )
            total_cost = import_details['total_cost'] or 0  # Chi phí mặc định là 0 nếu không có dữ liệu

            # Tính lợi nhuận
            total_revenue = entry['total_revenue']
            profit = total_revenue - total_cost

            # Thêm dữ liệu vào danh sách trả về
            data.append({
                "time": month.strftime('%m/%Y') if month else None,
                "medicine_name": medicine_name,
                "cost": f"{total_cost:,.0f}",  # Định dạng chi phí
                "revenue": f"{total_revenue:,.0f}",  # Định dạng doanh thu
                "profit": f"{profit:,.0f}",  # Định dạng lợi nhuận
            })

        return Response(data)
    

class ReportInventory(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            # Lấy tất cả thuốc
            medicines = Medicine.objects.all()

            # Tạo báo cáo tồn kho
            inventory_report = []

            for medicine in medicines:
                # Xác định trạng thái tồn kho của thuốc
                if medicine.stock_quantity == 0:
                    status_inventory = "Hết hàng"
                elif medicine.stock_quantity < 30:
                    status_inventory = "Gần hết hàng"
                else:
                    status_inventory = "Bình thường"

                # Thêm thông tin vào báo cáo
                inventory_report.append(
                    {
                        "medicine_name": medicine.medicine_name,
                        "stock_quantity": medicine.stock_quantity,
                        "status_inventory": status_inventory,
                    }
                )

            # Sắp xếp báo cáo theo số lượng tồn kho giảm dần
            inventory_report.sort(key=lambda x: x["stock_quantity"], reverse=True)

            # Trả về kết quả
            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": inventory_report,
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
                    "errorMessage": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReportImportReceipt(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            # Nhận các tham số từ request
            start_date = request.query_params.get("start_date", None)
            end_date = request.query_params.get("end_date", None)

            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if start_date and end_date and start_date > end_date:
                return Response(
                    {
                        "statuscode": status.HTTP_400_BAD_REQUEST,
                        "data": None,
                        "status": "error",
                        "errorMessage": "Ngày bắt đầu phải nhỏ hơn ngày kết thúc.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Lọc theo khoảng thời gian
            if start_date and end_date:
                receipts = ImportReceipt.objects.filter(
                    import_date__range=(start_date, end_date)
                )
            else:
                receipts = ImportReceipt.objects.all()

            report = []
            for receipt in receipts:
                employee_name = (
                    receipt.employee.full_name
                )  # Giả sử bạn có trường 'supplier' trong ImportReceipt

                # Lặp qua từng chi tiết của phiếu nhập
                for (
                    detail
                ) in (
                    receipt.details.all()
                ):  # Giả sử bạn có trường 'details' trong ImportReceipt
                    medicine = detail.medicine
                    total_cost = (
                        detail.quantity * detail.price
                    )  # Tổng chi phí của từng thuốc

                    report.append(
                        {
                            "id": receipt.id,
                            "import_date": receipt.import_date.strftime(
                                "%Y-%m-%d"
                            ),  # Ngày nhập
                            "employee_name": employee_name,  # Tên nhà cung cấp
                            "medicine_name": medicine.medicine_name,  # Tên thuốc
                            "quantity": detail.quantity,  # Số lượng nhập
                            "total_cost": total_cost,  # Tổng chi phí
                        }
                    )

            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": report,
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
                    "errorMessage": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReportEmployeeActivity(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            # Nhận các tham số từ request
            
            limit = request.query_params.get(
                "limit", None
            )  # Tham số số lượng nhân viên

            if limit:
                try:
                    limit = int(limit)
                except ValueError:
                    return Response(
                        {
                            "statuscode": status.HTTP_400_BAD_REQUEST,
                            "data": None,
                            "status": "error",
                            "errorMessage": "Tham số 'limit' phải là một số nguyên.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            
            receipts = ImportReceipt.objects.all()

            # Nhóm phiếu nhập theo nhân viên
            employee_report = {}
            for receipt in receipts:
                employee = receipt.employee
                if employee not in employee_report:
                    employee_report[employee] = {
                        "employee_name": employee.full_name,
                        "total_receipts": 0,
                        "total_quantity": 0,
                        "total_value": 0.0,  # Tổng giá trị nhập
                    }

                # Cập nhật số lần nhập, số lượng thuốc nhập và giá trị thuốc nhập
                employee_report[employee]["total_receipts"] += 1

                for (
                    detail
                ) in (
                    receipt.details.all()
                ):  # Giả sử có trường 'details' trong ImportReceipt
                    employee_report[employee]["total_quantity"] += detail.quantity
                    employee_report[employee]["total_value"] += (
                        detail.quantity * detail.price
                    )  # Giả sử 'price' là giá nhập của thuốc

            # Chuyển dữ liệu nhóm thành danh sách và sắp xếp theo tổng giá trị nhập giảm dần
            sorted_report_data = sorted(
                [
                    {
                        "employee_name": report["employee_name"],
                        "total_receipts": report["total_receipts"],
                        "total_quantity": report["total_quantity"],
                        "total_value": report["total_value"],
                    }
                    for report in employee_report.values()
                ],
                key=lambda x: x["total_value"],
                reverse=True,
            )

            # Lấy ra số lượng nhân viên theo tham số limit (nếu có)
            if limit is not None:
                sorted_report_data = sorted_report_data[:limit]

            return Response(
                {
                    "statuscode": status.HTTP_200_OK,
                    "data": sorted_report_data,
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
                    "errorMessage": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
>>>>>>> 221eb584e957ca1f61a11301cdea0185cb16971d

class ReportPatient(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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