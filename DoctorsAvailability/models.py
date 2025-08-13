# Models for doctors and patient appointments.

from django.db import models

class Doctor(models.Model):
    # Stores doctor details and availability.
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    # Stores patient appointments with doctors.
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient} with {self.doctor.name} on {self.date} at {self.time_slot}"
