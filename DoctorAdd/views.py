
from django.shortcuts import render
from .models import DoctorAdd

def doctor_list(request):
    doctors = DoctorAdd.objects.all()
    return render(request, 'DoctorAdd/doctor_list.html', {'doctors': doctors})



