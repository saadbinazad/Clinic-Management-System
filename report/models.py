# Create your models here.
from django.db import models
from django.utils import timezone

class Report(models.Model):
    DAILY = 'daily'
    MONTHLY = 'monthly'
    REPORT_TYPE_CHOICES = [(DAILY, 'Daily'), (MONTHLY, 'Monthly')]

    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    date = models.DateField(default=timezone.now)
    total_patients = models.PositiveIntegerField()
    total_appointments = models.PositiveIntegerField()
    total_nurses = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.report_type.title()} Report - {self.date}"

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient_name} with {self.doctor_name} on {self.date:%Y-%m-%d %H:%M}"
