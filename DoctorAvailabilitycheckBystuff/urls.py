from django.urls import path
from . import views

urlpatterns = [
    path("", views.check_availability, name="check_availability"),
    path("book/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
]
