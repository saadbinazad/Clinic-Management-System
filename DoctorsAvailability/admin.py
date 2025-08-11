from django.contrib import admin

from.models import Doctor, Appointment

class AppointmentAdmin(admin.ModelAdmin):

 list_display = ['doctor','patient','date','time_slot','is_confirmed','is_cancelled']

 list_editable = ['is_confirmed',' is_cancelled']


#Register both models to manage them through admin site 

admin .site. register(Doctor)
admin .site. register(Appointment, AppointmentAdmin) 