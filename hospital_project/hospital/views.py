from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Patient, Doctor, Appointment
from django.db import IntegrityError

def home(request):
    """
    Renders the homepage with real statistics.
    """
    from datetime import date
    
    # Get real statistics
    total_patients = Patient.objects.filter(status='Admitted').count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    todays_appointments = Appointment.objects.filter(appointment_date=date.today()).count()
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'todays_appointments': todays_appointments,
    }
    return render(request, 'hospital/home.html', context)

def patient_list(request):
    """
    Displays a list of all admitted patients.
    """
    patients = Patient.objects.filter(status='Admitted').order_by('-admission_date')
    return render(request, 'hospital/patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    """
    Displays detailed information about a specific patient.
    """
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        if 'clear_payment' in request.POST:
            patient.payment_status = 'Cleared'
            patient.save()
            messages.success(request, f'Payment has been cleared for {patient.first_name} {patient.last_name}.')
            return redirect('patient_detail', patient_id=patient.id)
    
    # Get appointments for this patient
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')
    
    context = {
        'patient': patient,
        'appointments': appointments
    }
    return render(request, 'hospital/patient_detail.html', context)

def add_patient(request):
    """
    Handles the logic for admitting a new patient.
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        
        # For simplicity, we assume seats are always available.
        # In a real app, you'd check room/bed availability here.
        
        try:
            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                contact_no=contact_no,
                email=email
            )
            # Success message
            messages.success(request, f'Patient {patient.first_name} {patient.last_name} has been successfully admitted. A confirmation has been sent.')
            return redirect('home')
        except IntegrityError:
            # Handle the case where email already exists
            messages.error(request, f'A patient with email "{email}" already exists in the system. Please use a different email address.')
            return render(request, 'hospital/add_patient.html')

    return render(request, 'hospital/add_patient.html')

def remove_patient(request):
    """
    Handles logic for discharging a patient after checking payment status.
    """
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = get_object_or_404(Patient, id=patient_id)

        if patient.payment_status == 'Cleared':
            patient.status = 'Discharged'
            patient.save()
            messages.success(request, f'Payment cleared. Patient {patient.first_name} has been released. Payment slip sent.')
        else:
            messages.error(request, f'Payment for {patient.first_name} is still pending. Please clear the payment before discharge.')
        
        return redirect('remove_patient')

    # We only show admitted patients in the dropdown for discharge
    admitted_patients = Patient.objects.filter(status='Admitted')
    return render(request, 'hospital/remove_patient.html', {'patients': admitted_patients})


def schedule_appointment(request):
    """
    Handles the logic for scheduling a new appointment.
    """
    doctors = Doctor.objects.all()
    # For this feature, we need a way to identify the patient scheduling.
    # In a real system, this would come from a logged-in user session.
    # For now, we'll list existing patients in a dropdown.
    patients = Patient.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        app_date = request.POST.get('appointment_date')
        app_time = request.POST.get('appointment_time')
        purpose = request.POST.get('purpose')

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        try:
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=app_date,
                appointment_time=app_time,
                purpose=purpose
            )
            messages.success(request, f'Appointment approved for {patient.first_name} with {doctor.name}. Please attend on time.')
        except IntegrityError:
            # This error is raised if the (doctor, date, time) combination is not unique
            messages.error(request, f'This slot with {doctor.name} is already booked. Please choose a different slot.')
        
        return redirect('schedule_appointment')

    context = {
        'doctors': doctors,
        'patients': patients
    }
    return render(request, 'hospital/schedule_appointment.html', context)

def appointment_list(request):
    """
    Displays a list of all scheduled appointments.
    """
    appointments = Appointment.objects.all().order_by('appointment_date', 'appointment_time')
    return render(request, 'hospital/appointment_list.html', {'appointments': appointments})

def edit_appointment(request, appointment_id):
    """
    Handles editing an existing appointment.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        app_date = request.POST.get('appointment_date')
        app_time = request.POST.get('appointment_time')
        purpose = request.POST.get('purpose')

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        try:
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.appointment_date = app_date
            appointment.appointment_time = app_time
            appointment.purpose = purpose
            appointment.save()
            
            messages.success(request, f'Appointment for {patient.first_name} with {doctor.name} has been updated successfully.')
            return redirect('appointment_list')
        except IntegrityError:
            messages.error(request, f'This slot with {doctor.name} is already booked. Please choose a different slot.')
    
    context = {
        'appointment': appointment,
        'doctors': doctors,
        'patients': patients
    }
    return render(request, 'hospital/edit_appointment.html', context)

def delete_appointment(request, appointment_id):
    """
    Handles deleting an appointment.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        patient_name = f"{appointment.patient.first_name} {appointment.patient.last_name}"
        doctor_name = appointment.doctor.name
        appointment.delete()
        messages.success(request, f'Appointment for {patient_name} with {doctor_name} has been cancelled successfully.')
        return redirect('appointment_list')
    
    return render(request, 'hospital/delete_appointment.html', {'appointment': appointment})