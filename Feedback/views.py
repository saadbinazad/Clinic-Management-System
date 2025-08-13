from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm

@login_required
# View to handle feedback/complaint submission by logged-in users
# Displays form, handles validation, and provides success/error messages

def submit_feedback(request):
    # Allows logged-in patients to submit feedback or complaints
    if request.method == 'POST':
        # Bind form with POST data and uploaded files
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            # Save feedback with current user
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            # Show success message and redirect
            messages.success(request, "Your feedback has been submitted successfully.")
            return redirect('feedback')   # Redirect after success
    else:
        # If not POST, or form invalid, show error and empty form
        messages.error(request, "Please fill in all required fields.")
        form = FeedbackForm()
    # Render the feedback form template
    return render(request, 'feedback_form.html', {'form': form})





