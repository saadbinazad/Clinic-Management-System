# Register your models here.
from django.contrib import admin
from .models import Nurse, Patient

admin.site.register(Nurse)
admin.site.register(Patient)
