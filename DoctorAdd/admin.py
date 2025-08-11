from django.contrib import admin 

from .models import Doctor, DoctorAdd

class DoctorAddAdmin(admin.ModelAdmin): 
    
 list_display = ('get_name', 'department', 'Id','Specialization' ,'schedule' ,'add_confirm' ,'add_error','mobile', 'status')
 
search_fields = ('user__first_name', 'user__last_name', 'department')
    
list_editable= ['add_confirm' ,'add_error']

admin.site.register(Doctor ,DoctorAdd, DoctorAddAdmin)


