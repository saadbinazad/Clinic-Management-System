# Models for storing patient feedback and complaints.

from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    # Stores patient feedback or complaints.
    CATEGORY_CHOICES = [
        ('complaint','complaint'),
        ('suggestion','suggestion'),
        ('other','other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to patient
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # Type of feedback
    messages = models.TextField()  # Feedback message
    # screenshot = models.ImageField(upload_to='feedback_screenshot/',blank=True, null=True)  # Optional screenshot
    created_at = models.DateField(auto_now_add=True)  # Submission date

    def __str__(self):
        return f"{self.user.username} - {self.category}"  # String representation for admin


