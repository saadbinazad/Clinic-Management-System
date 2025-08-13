from django.contrib import admin
from .models import DoctorAdd

@admin.register(DoctorAdd)
class DoctorAddAdmin(admin.ModelAdmin):
    list_display = ('get_name',  'department', 'specialization', 'schedule', 'mobile', 'status')
    search_fields = ('user__first_name', 'user__last_name', 'department')
    list_editable = ('status',)

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = "Name"



