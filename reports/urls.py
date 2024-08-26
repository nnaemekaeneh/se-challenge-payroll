
from django.contrib import admin
from django.urls import path, include
from reports.views import PayrollReport


urlpatterns = [
    path("", PayrollReport.as_view(), name='payroll'),
]
