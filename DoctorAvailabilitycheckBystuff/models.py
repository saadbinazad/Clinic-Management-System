from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from DoctorAddByAdmin.models import Doctor

class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    start_time = models.TimeField()  # inclusive
    end_time = models.TimeField()    # exclusive
    slot_minutes = models.PositiveIntegerField(default=30)

    class Meta:
        unique_together = ("doctor", "date", "start_time", "end_time")
        ordering = ["date", "start_time"]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.doctor} {self.date} {self.start_time}-{self.end_time}"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    patient_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("doctor", "date", "time")
        ordering = ["-created_at"]

    def clean(self):
        if self.date < timezone.localdate():
            raise ValidationError("Cannot book in the past.")

    def __str__(self):
        return f"{self.patient_name} with {self.doctor} on {self.date} at {self.time}"

