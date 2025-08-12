# Create your views here.
from django.shortcuts import render
from django.utils import timezone
from .forms import ReportFilterForm
from NurseAssignment.models import Nurse, Patient
from .models import Appointment

def daily_monthly_report(request):
    form = ReportFilterForm(request.POST or None, initial={'date': timezone.now().date()})
    report = None

    if form.is_valid():
        rt, date = form.cleaned_data['report_type'], form.cleaned_data['date']

        if rt == 'daily':
            appointments = Appointment.objects.filter(date__date=date)
        else: 
            appointments = Appointment.objects.filter(date__year=date.year, date__month=date.month)

        report = {
            'type': rt.title(),
            'date': date,
            'total_patients': Patient.objects.count(),
            'total_appointments': appointments.count(),
            'total_nurses': Nurse.objects.count(),
        }

    return render(request, 'report/report.html', {'form': form, 'report': report})
