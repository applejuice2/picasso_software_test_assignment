from django.db import models
from django.core.validators import MaxValueValidator

class Incident(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True, 
        validators=[MaxValueValidator(999999999)],
    )
    original_crime_type_name = models.CharField(
        max_length=50,
    )
    report_date = models.DateTimeField()
    call_date = models.DateTimeField()
    offense_date = models.DateTimeField()
    call_time = models.TimeField()
    call_date_time = models.DateTimeField()
    disposition = models.CharField(
        max_length=12,
    )
    adress = models.CharField(
        max_length=50,
    )
    city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    state = models.CharField(
        max_length=50,
    )
    agency_id = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999999)],
    )
    adress_type = models.CharField(
        max_length=50,
    )
    common_location = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['id']

