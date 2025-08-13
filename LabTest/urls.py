# URL patterns for lab test listing and booking.

from django.urls import path
from . import views

urlpatterns = [
    path('labtests/', views.lab_test_list, name='labtest_list'),
    path('labtests/book/<int:test_id>/', views.book_lab_test, name='book_lab_test'),
]
