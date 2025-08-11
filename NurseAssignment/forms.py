# nurse assignment forms
from django import forms
from .models import Nurse, Patient

class NurseAssignmentForm(forms.Form):
    nurse = forms.ModelChoiceField(queryset=Nurse.objects.all(), label="Select Nurse")
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), label="Select Patient")
