# Models for lab tests and patient lab test bookings.

from django.db import models
from django.contrib.auth.models import User

class LabTest(models.Model):
    # Stores available lab tests with details.
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50)
    sample_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class LabTestBooking(models.Model):
    # Stores patient bookings for lab tests.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lab_test.name} on {self.date} at {self.time}"
