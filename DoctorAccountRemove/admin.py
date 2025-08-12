from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DoctorAccountRemove

@admin.register(DoctorAccountRemove)
class DoctorAccountRemoveAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor_name', 'removed_on')
    search_fields = ('doctor_name',)

