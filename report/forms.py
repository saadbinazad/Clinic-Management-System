from django import forms

class ReportFilterForm(forms.Form):
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
    ]

    report_type = forms.ChoiceField(choices=REPORT_TYPE_CHOICES)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
