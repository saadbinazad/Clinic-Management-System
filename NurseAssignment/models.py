# nurse assignment
from django.db import models

class Nurse(models.Model):
    name = models.CharField(max_length=100)
    max_patients = models.PositiveIntegerField(default=5) 

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name

class NurseAssignment(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='assignments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nurse', 'patient') 

    def __str__(self):
        return f"{self.nurse.name} assigned to {self.patient.name}"
