from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from incidents.models import Incident
from api.serializers import IncidentSerializer
from .filters import ReportDateFilter


class IncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReportDateFilter

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
