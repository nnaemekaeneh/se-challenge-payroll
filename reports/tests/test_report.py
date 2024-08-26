from django.test import Client
from django.urls import resolve, reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import RequestsClient

from reports.views import PayrollReport




class TestReportUrls(TestCase):

    def setUp(self):
        self.client = Client()
        self.payroll_url = reverse("payroll")

    def test_payroll_list_view_url(self):
        response = self.client.get(self.payroll_url)

        self.assertEqual(
            resolve(self.payroll_url).func.view_class, PayrollReport
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payroll_post_request_fail(self):

        with open('reports/tests/time-report-x.csv') as file:
            response = self.client.post(self.payroll_url, {'csvFile': file})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_payroll_post_request_pass(self):

        with open('reports/tests/time-report-41.csv') as file:
            response = self.client.post(self.payroll_url, {'csvFile': file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
