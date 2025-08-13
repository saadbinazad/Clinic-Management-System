# Views for listing lab tests and handling patient lab test bookings.

from django.shortcuts import render, redirect
from .models import LabTest, LabTestBooking
from .forms import LabTestBookingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def lab_test_list(request):
    # Display a list of available lab tests for patients to browse.
    tests = LabTest.objects.all()
    return render(request, 'labtest_list.html', {'tests': tests})

@login_required
def book_lab_test(request, test_id):
    # Allow patients to book a selected lab test by providing date, time, and location.
    # Show confirmation or error messages as needed.
    test = LabTest.objects.get(id=test_id)
    if request.method == 'POST':
        form = LabTestBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.lab_test = test
            booking.save()
            messages.success(request, 'Lab test booked successfully!')
            # Notify lab here (e.g., send email)
            return redirect('labtest_list')
        else:
            messages.error(request, 'Please fill all required fields.')
    else:
        form = LabTestBookingForm(initial={'lab_test': test})
    return render(request, 'book_lab_test.html', {'form': form, 'test': test})
