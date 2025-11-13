from django.contrib import admin
from .models import UserProfile, NotificationLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'telegram_chat_id']
    search_fields = ['user__username', 'user__email', 'phone']

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel_used', 'success', 'priority', 'created_at']
    list_filter = ['channel_used', 'success', 'priority', 'created_at']
    search_fields = ['user__username', 'message', 'subject']
    readonly_fields = ['created_at']
