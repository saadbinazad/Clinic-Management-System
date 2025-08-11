from django.contrib import admin

from .models import Feedback

@admin.register(Feedback)

class FeedbackAdmin (admin.ModelAdmin):

    
    #Admin panel settings for managing Feedback

    list_display = ('user','category','reviewed','created_at')
    
    list_filter = ('category','reviewed')

    search_fields = ('user_username','message')
