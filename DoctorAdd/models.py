from django.db import models
from django.contrib.auth.models import User

class DoctorAdd(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    schedule = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
