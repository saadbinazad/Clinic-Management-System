from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient-list/', views.patient_list, name='patient_list'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('remove-patient/', views.remove_patient, name='remove_patient'),
    path('schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('appointment-list/', views.appointment_list, name='appointment_list'),
    path('appointment/<int:appointment_id>/edit/', views.edit_appointment, name='edit_appointment'),
    path('appointment/<int:appointment_id>/delete/', views.delete_appointment, name='delete_appointment'),
]