import pandas
import datetime as dt
from itertools import chain

from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK
from rest_framework.renderers import TemplateHTMLRenderer

from reports.models import EmployeePayReport
from .payroll_labels import (
    YEAR_2023,
    REPORT_TITLE,
    FILE_TYPE,
    DATE,
    HOURS_WORKED,
    EMPLOYEE_ID,
    JOB_GROUP,
    GROUP_A,
    GROUP_B,
)


class BaseView(APIView):
    renderer_classes = [TemplateHTMLRenderer]


class PayrollReport(BaseView):
    template_name = "payroll_report.html"

    def get(self, request, *args, **kwargs):

        employee_reports = self.get_employee_report()

        data = {"payrollReport": employee_reports}

        print(data)

        return Response(data=data)

    def post(self, request, *args, **kwargs):
        GET = request.data
        status = HTTP_405_METHOD_NOT_ALLOWED
        file = GET.get("csvFile", None)

        try:
            file_name = file.name
            data = pandas.read_csv(file)
            checker = self.file_checker(file_name, data)

            if checker:
                report_id = int(file_name[12:-4])

                if not EmployeePayReport.objects.filter(report_id=report_id).exists():

                    data = data.reset_index()

                    for index, row in data.iterrows():

                        employee_report = EmployeePayReport(
                            employee=row[EMPLOYEE_ID],
                            report_id=report_id,
                            hours_worked=row[HOURS_WORKED],
                            job_group=row[JOB_GROUP],
                            work_date=dt.datetime.strptime(
                                row[DATE], "%d/%m/%Y"
                            ).strftime("%Y-%m-%d"),
                        )
                        employee_report.save()
                    status = HTTP_200_OK

        except Exception as e:
            print("Error", e)

        return Response(status=status)

    def get_employee_report(self):

        employeeReports = []

        for month in YEAR_2023:
            first_half_start = month["first_half"]["start_date"]
            first_half_end = month["first_half"]["end_date"]
            second_half_start = month["second_half"]["start_date"]
            second_half_end = month["second_half"]["end_date"]

            first_half_report = (
                EmployeePayReport.objects.filter(
                    work_date__range=[first_half_start, first_half_end]
                )
                .order_by("employee")
                .values("employee", "hours_worked", "work_date", "job_group")
            )

            second_half_report = (
                EmployeePayReport.objects.filter(
                    work_date__range=[second_half_start, second_half_end]
                )
                .order_by("employee")
                .values("employee", "hours_worked", "work_date", "job_group")
            )

            first_half_report = self.parse_report(
                first_half_start, first_half_end, first_half_report
            )
            union_set = chain(first_half_report, second_half_report)
            print("UNON: ", union_set.objects.all())

            if first_half_report:
                employeeReports.extend(first_half_report)


            second_half_report = self.parse_report(
                second_half_start, second_half_end, second_half_report
            )

            print("second_half_report", second_half_report)

            if second_half_report:
                employeeReports.extend(second_half_report)

        data = {"employeeReports": employeeReports}

        return data

    def parse_report(self, start_date, end_date, payroll_data):

        employeeReports = []
        employee_ids = payroll_data.values_list("employee", flat=True).distinct(
            "employee"
        )

        for employee_id in employee_ids:
            employee_pay_roll = EmployeePayReport.objects.filter(
                employee=employee_id
            ).first()

            employee_stats = {
                "employeeId": employee_id,
            }
            payPeriod = {
                "startDate": start_date,
                "endDate": end_date,
            }

            if employee_pay_roll.job_group == GROUP_A:

                total_hours_A = payroll_data.filter(
                    employee=employee_id, job_group=GROUP_A
                ).aggregate(Sum("hours_worked"))

                if total_hours_A["hours_worked__sum"] != None:
                    amountPaid = total_hours_A["hours_worked__sum"] * 20
                    employee_stats["amountPaid"] = f"${amountPaid}"
                    employee_stats["payPeriod"] = payPeriod
                    employeeReports.append(employee_stats)

            else:

                total_hours_B = payroll_data.filter(
                    employee=employee_id, job_group=GROUP_B
                ).aggregate(Sum("hours_worked"))

                total_hours_B = payroll_data.filter(
                    employee=employee_id, job_group=GROUP_B
                ).aggregate(Sum("hours_worked"))

                if total_hours_B["hours_worked__sum"] != None:
                    amountPaid = total_hours_B["hours_worked__sum"] * 30
                    employee_stats["amountPaid"] = f"${amountPaid}"
                    employee_stats["payPeriod"] = payPeriod
                    employeeReports.append(employee_stats)

        return employeeReports

    def file_checker(self, file_name, data):
        result = False
        try:
            if (
                file_name[:12] == REPORT_TITLE
                and file_name[12:-4].isnumeric()
                and file_name[-4:] == FILE_TYPE
            ):
                if (
                    DATE in data
                    and HOURS_WORKED in data
                    and EMPLOYEE_ID in data
                    and JOB_GROUP in data
                ):
                    if data.isnull().values.any():
                        result = False
                    else:
                        result = True
        except:
            print("Failed to conform CSV File")

        return result
