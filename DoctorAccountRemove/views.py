from django.shortcuts import render
from .models import DoctorAccountRemove

def removal_list(request):
    removals = DoctorAccountRemove.objects.all()
    return render(request, 'DoctorAccountRemove/removal_list.html', {'removals': removals})

