# URL patterns for doctor listing and appointment booking.

from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for listing doctors
    path('', views.doctor_list, name='doctor_list'),

    # URL pattern for booking an appointment with a specific doctor
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
]
