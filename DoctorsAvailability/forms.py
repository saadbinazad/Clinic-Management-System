# Forms for doctor appointment booking by patients.

from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    # Form for patients to book appointments with doctors.

    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'date', 'time_slot']
