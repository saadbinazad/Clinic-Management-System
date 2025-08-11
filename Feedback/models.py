from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):

    #stores patient feedback or complaints .

    CATEGORY_CHOICES = [
        ('complaint','complaint'),
        ('suggestion','suggestion'),
        ('other','other'),
    ]

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    messages = models.TextField()
    screenshot = models.ImageField(upload_to='feedback_screenshot/',blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str_(self):

     return f"{self.user.username} - {self.category}"


