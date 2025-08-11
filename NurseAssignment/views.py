# Create your views here.
# nurse_assignment/views.py
from django.shortcuts import render
from .forms import NurseAssignmentForm
from .models import NurseAssignment, Nurse

def assign_nurse(request):
    message = None
    error = None

    if request.method == "POST":
        form = NurseAssignmentForm(request.POST)
        if form.is_valid():
            nurse = form.cleaned_data['nurse']
            patient = form.cleaned_data['patient']

            if NurseAssignment.objects.filter(nurse=nurse, patient=patient).exists():
                error = "This nurse is already assigned to this patient."
            else:
                assigned_count = NurseAssignment.objects.filter(nurse=nurse).count()
                if assigned_count >= nurse.max_patients:
                    error = f"Nurse {nurse.name} has reached the maximum number of patients."
                else:
                    NurseAssignment.objects.create(nurse=nurse, patient=patient)
                    message = "Nurse assigned successfully."
                    form = NurseAssignmentForm()
        else:
            error = "Please select both nurse and patient."
    else:
        form = NurseAssignmentForm()

    nurseassignment_list = NurseAssignment.objects.all()

    context = {
        "form": form,
        "message": message,
        "error": error,
        "nurseassignment_list": nurseassignment_list,
    }
    return render(request, "nurse_assignment/assign.html", context)
