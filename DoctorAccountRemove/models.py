from django.db import models

class DoctorAccountRemove(models.Model):
    doctor_name = models.CharField(max_length=100)
    reason = models.TextField(blank=True, null=True)
    removed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doctor_name
