from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_monthly_report, name='daily_monthly_report'),
]
