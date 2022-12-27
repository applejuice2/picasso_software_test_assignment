from django_filters.rest_framework import FilterSet, DateFromToRangeFilter

from incidents.models import Incident
from .fields import CustomDateRangeField


class CustomDateRangeFilter(DateFromToRangeFilter):
    field_class = CustomDateRangeField


class ReportDateFilter(FilterSet):
    date = CustomDateRangeFilter(field_name='report_date')

    class Meta:
        model = Incident
        fields = ['date']
