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
        # get all the payrollReport in the database
        data = {"payrollReport": employee_reports}

        print(data)

        return Response()

    def post(self, request, *args, **kwargs):
        GET = request.data
        status = HTTP_405_METHOD_NOT_ALLOWED
        file = GET.get("csvFile", None)

        try:
            # get file name
            file_name = file.name

            data = pandas.read_csv(file)

            # if true file is valid
            checker = self.file_checker(file_name, data)

            if checker:
                # gets the report_id from filename
                report_id = int(file_name[12:-4])

                # if the report id does not exisits data can be saved
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
        """Get the employees payroll report from JAN - DEC"""

        employeeReports = []

        for month in YEAR_2023:
            first_half_start = month["first_half"]["start_date"]
            first_half_end = month["first_half"]["end_date"]
            second_half_start = month["second_half"]["start_date"]
            second_half_end = month["second_half"]["end_date"]

            # report per month from 1 - 28/30/31
            month_reports = (
                EmployeePayReport.objects.filter(
                    work_date__range=[first_half_start, second_half_end]
                )
                .order_by("employee", "work_date")
                .values("employee", "hours_worked", "work_date", "job_group")
            )
            # distinct employees id that are in that month
            employee_ids = month_reports.values_list("employee", flat=True).distinct(
                "employee"
            )

            for id in employee_ids:
                employee = EmployeePayReport.objects.filter(employee=id).first()

                first_half_data = month_reports.filter(
                    employee=id,
                    work_date__range=[first_half_start, first_half_end],
                )
                # report for first half of the month
                first_half_report = self.parse_report(
                    first_half_start, first_half_end, employee, first_half_data
                )
                if first_half_report:
                    employeeReports.append(first_half_report)

                # report for second half of the month
                second_half_data = month_reports.filter(
                    employee=id,
                    work_date__range=[second_half_start, second_half_end],
                )
                second_half_report = self.parse_report(
                    second_half_start, second_half_end, employee, second_half_data
                )
                if second_half_report:
                    employeeReports.append(second_half_report)

        data = {"employeeReports": employeeReports}

        return data

    def parse_report(self, start_date, end_date, employee, payroll_data):
        """Parse Report according to total hours and Job group"""
        employee_stats = {
            "employeeId": employee.employee,
            "payPeriod": {
                "startDate": start_date,
                "endDate": end_date,
            },
        }

        # total hours works per employee
        total_hours = payroll_data.aggregate(Sum("hours_worked"))
        first_half_total_hours = total_hours["hours_worked__sum"]

        if employee.job_group == GROUP_A and first_half_total_hours != None:
            # Group A total amount earn for a half
            amountPaid = first_half_total_hours * 20
            employee_stats["amountPaid"] = f"${amountPaid}"
            return employee_stats

        elif employee.job_group == GROUP_B and first_half_total_hours != None:
            # Group B total amount earn for a half
            amountPaid = first_half_total_hours * 30
            employee_stats["amountPaid"] = f"${amountPaid}"
            return employee_stats

    def file_checker(self, file_name, data):
        """Checks if the file meets the specification"""
        result = False
        try:
            # checks if filename follows:
            # filename title formart time-report-
            # report_id is numerical
            # it is of type csv
            if (
                file_name[:12] == REPORT_TITLE
                and file_name[12:-4].isnumeric()
                and file_name[-4:] == FILE_TYPE
            ):
                # checks if this columns are in the data
                if (
                    DATE in data
                    and HOURS_WORKED in data
                    and EMPLOYEE_ID in data
                    and JOB_GROUP in data
                ):
                    # check if there is a null value
                    if data.isnull().values.any():
                        result = False
                    else:
                        result = True
        except:
            print("Failed to conform CSV File")

        return result
