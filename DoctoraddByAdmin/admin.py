from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "email", "phone", "active", "created_at")
    list_filter = ("active", "specialization")
    search_fields = ("name", "email", "phone")

