from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .forms import DoctorForm
from .models import Doctor

@require_http_methods(["GET", "POST"])
def add_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Doctor added successfully.")
                return redirect("doctor_list")
            except Exception as e:
                messages.error(request, f"System error: {e}")
        else:
            messages.error(request, "Please fix validation errors.")
    else:
        form = DoctorForm()
    return render(request, "doctors/add_doctor.html", {"form": form})

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctors/doctor_list.html", {"doctors": doctors})
