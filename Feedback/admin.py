# Admin configuration for managing patient feedback and complaints.

from django.contrib import admin

from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Admin panel settings for managing Feedback
    list_display = ('user', 'category', 'created_at')  # Columns shown in admin list
    list_filter = ('category',)  # Filter by category
    search_fields = ('user__username', 'messages')  # Search by username and message
