from django import forms
from django.utils import timezone
from .models import Appointment

class AvailabilitySearchForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def clean_date(self):
        d = self.cleaned_data["date"]
        if d < timezone.localdate():
            raise forms.ValidationError("Past date is not allowed.")
        return d

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient_name"]
