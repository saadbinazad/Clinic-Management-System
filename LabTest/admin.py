from django.contrib import admin
from .models import LabTest, LabTestBooking

# Register the LabTest model with the admin site
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'sample_type']
    search_fields = ['name']

# Register the LabTestBooking model with the admin site
class LabTestBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'lab_test', 'date']
    list_filter = ['date']
    search_fields = ['user__username', 'lab_test__name']

# Register both models
admin.site.register(LabTest, LabTestAdmin)
admin.site.register(LabTestBooking, LabTestBookingAdmin)
