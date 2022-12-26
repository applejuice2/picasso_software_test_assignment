from django.urls import path

from .views import IncidentList

app_name = 'api'

urlpatterns = [
    path('incidents/', IncidentList.as_view(), name='incidents'),
]