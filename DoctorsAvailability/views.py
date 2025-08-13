# Views for listing doctors and handling patient appointment bookings.

from django.shortcuts import render, redirect
from .models import Doctor, Appointment
from .forms import AppointmentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def doctor_list(request):
    # Display a list of available doctors for patients to browse.
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    # Allow patients to book an appointment with a selected doctor.
    # Show confirmation or error messages as needed.
    doctor = Doctor.objects.get(id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            # Notify doctor here (e.g., send email)
            return redirect('doctor_list')
        else:
            messages.error(request, 'Please fill all required fields.')
    else:
        form = AppointmentForm(initial={'doctor': doctor})
    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})

