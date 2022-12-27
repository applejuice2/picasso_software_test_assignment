from django_filters.fields import DateRangeField

from .widgets import CustomDateRangeWidget


class CustomDateRangeField(DateRangeField):
    widget = CustomDateRangeWidget
