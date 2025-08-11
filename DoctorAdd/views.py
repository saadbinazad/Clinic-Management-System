
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Doctor
from .forms import DoctorForm

def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user  # যদি doctor লগইন করা user হয়
            doctor.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctor_add.html', {'form': form})

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


