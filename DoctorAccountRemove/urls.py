from django.urls import path
from . import views

app_name = 'DoctorAccountRemove'

urlpatterns = [
    path('', views.removal_list, name='removal_list'),
]
