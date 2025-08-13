from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from DoctorAddByAdmin.models import Doctor
from .forms import AvailabilitySearchForm, AppointmentForm
from .models import AvailabilitySlot, Appointment
from .utils import iter_slots

@require_http_methods(["GET", "POST"])
def check_availability(request):
    """
    Receptionist selects a date -> system shows matching availability.
    Shows doctors with selectable time slots.
    """
    form = AvailabilitySearchForm(request.GET or None)
    context = {"form": form, "results": []}

    if form.is_valid():
        selected_date = form.cleaned_data["date"]
        slots = AvailabilitySlot.objects.filter(date=selected_date, doctor__active=True)
        results = []
        for slot in slots.select_related("doctor"):
            taken_times = set(
                Appointment.objects.filter(doctor=slot.doctor, date=selected_date)
                .values_list("time", flat=True)
            )
            available_times = [t for t in iter_slots(slot.start_time, slot.end_time, slot.slot_minutes)
                               if t not in taken_times]
            results.append({
                "doctor": slot.doctor,
                "slot": slot,
                "available_times": available_times
            })
        context["results"] = [r for r in results if r["available_times"]]
        if not context["results"]:
            messages.info(request, "No availability.")
    elif request.GET:
        messages.error(request, "Invalid input.")

    return render(request, "availability/check_availability.html", context)

@require_http_methods(["POST"])
def book_appointment(request, doctor_id):
    """
    Books an appointment and refreshes the page -> 'real-time' update.
    """
    doctor = get_object_or_404(Doctor, pk=doctor_id, active=True)
    date_str = request.POST.get("date")
    time_str = request.POST.get("time")
    patient_name = request.POST.get("patient_name", "").strip()

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%H:%M").time()
    except Exception:
        messages.error(request, "Invalid input.")
        return redirect("check_availability")

    if date_obj < timezone.localdate():
        messages.error(request, "Past date is not allowed.")
        return redirect(f"{request.META.get('HTTP_REFERER','/availability/')}")

    # Ensure time is inside a defined slot for the doctor on that date
    ok = AvailabilitySlot.objects.filter(
        doctor=doctor, date=date_obj,
        start_time__lte=time_obj, end_time__gt=time_obj
    ).exists()
    if not ok:
        messages.error(request, "No availability.")
        return redirect("check_availability")

    try:
        Appointment.objects.create(
            doctor=doctor, date=date_obj, time=time_obj, patient_name=patient_name or "Walk-in"
        )
        messages.success(request, "Appointment booked.")
    except Exception as e:
        # duplicate or DB/network error
        messages.error(request, f"Error while booking: {e}")

    # Redirect back to same date so UI updates immediately
    return redirect(f"/availability/?date={date_obj.isoformat()}")
