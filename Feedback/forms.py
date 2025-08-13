# Forms for patient feedback and complaints submission.

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    # Form for patients to submit feedback or complaints.
    class Meta:
        model = Feedback
        fields = ['category','messages']  # Fields shown in the form
