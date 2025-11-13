from django.db import models
from django.contrib.auth.models import User


class NotificationChannel(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    TELEGRAM = 'telegram', 'Telegram'


class NotificationPriority(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)
    preferred_channels = models.JSONField(default=list)  # Список предпочтительных каналов

    def __str__(self):
        return f"{self.user.username} Profile"


class NotificationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    channel_used = models.CharField(max_length=20, choices=NotificationChannel.choices)
    priority = models.CharField(max_length=10, choices=NotificationPriority.choices,
                                default=NotificationPriority.MEDIUM)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    retry_attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.user.username} via {self.channel_used}"
    