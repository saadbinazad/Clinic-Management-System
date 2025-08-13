# Views for handling feedback and complaints submission by patients.

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm

@login_required
def submit_feedback(request):
    # Allows logged-in patients to submit feedback or complaints.
    # Handles form validation, saving, and user notifications.
    if request.method == 'POST':
        form = FeedbackForm(request.POST,request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Link feedback to current user
            feedback.save()
            messages.success(request, "Your feedback has been submitted successfully.")
            return redirect ('feedback')   # Redirect after success
    else:
        messages.error(request, "Please fill in all required fields.")
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})





