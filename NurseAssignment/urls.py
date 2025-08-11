# nurse_assignment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('assign/', views.assign_nurse, name='assign_nurse'),
]
