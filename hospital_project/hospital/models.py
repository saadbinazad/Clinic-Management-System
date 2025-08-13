# In hospital/models.py

from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    """
    Represents a doctor in the hospital.
    """
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialty})"

class Patient(models.Model):
    """
    Represents a patient admitted to the hospital.
    """
    STATUS_CHOICES = [
        ('Admitted', 'Admitted'),
        ('Discharged', 'Discharged'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Cleared', 'Cleared'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    admission_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Admitted')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    """
    Represents an appointment scheduled by a patient with a doctor.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    purpose = models.TextField()

    class Meta:
        # Ensures a doctor cannot have two appointments at the exact same time
        unique_together = ('doctor', 'appointment_date', 'appointment_time')

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.appointment_date} at {self.appointment_time}"
