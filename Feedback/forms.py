from django import forms
from .models import Feedback

class FeedbackForm (forms.ModelForm):
    
    #Form for Patients to submit feedback or complaints

 class Meta:

    model = Feedback
    fields = ['category','message','screenshot']
