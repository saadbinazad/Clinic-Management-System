from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["name", "specialization", "email", "phone", "active"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit():
            raise forms.ValidationError("Phone must be digits only.")
        if len(phone) < 8:
            raise forms.ValidationError("Phone seems too short.")
        return phone
