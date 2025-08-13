# Forms for lab test booking by patients.

from django import forms

from .models import LabTest, LabTestBooking


class LabTestBookingForm(forms.ModelForm):
    # Form for patients to book lab tests.
    class Meta:
        model = LabTestBooking
        fields = ['lab_test', 'date', 'time', 'location']
