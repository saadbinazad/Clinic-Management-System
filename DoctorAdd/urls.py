from django.urls import path
from . import views

app_name = 'DoctorAdd'

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
]
