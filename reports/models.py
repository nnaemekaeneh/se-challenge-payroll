from django.db import models


# Employee Model
class EmployeePayReport(models.Model):
    employee = models.SmallIntegerField("Employee ID", null=False, blank=False)
    report_id = models.SmallIntegerField("Report ID", null=False, blank=False)
    hours_worked = models.DecimalField(
        "Hours Worked", max_digits=5, decimal_places=2, default=0.0
    )
    job_group = models.CharField("Job Group", max_length=1, null=False, blank=False)
    work_date = models.DateField("Work Date", blank=False, null=False)
    created = models.DateTimeField("Created", null=False, auto_now_add=True)
    updated = models.DateTimeField("Updated", auto_now=True, null=False)
