from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .base import BaseNotificationProvider
from notification_system.models import NotificationChannel


class EmailProvider(BaseNotificationProvider):

    def __init__(self):
        super().__init__()
        self.channel_type = NotificationChannel.EMAIL

    def is_available(self, user: User) -> bool:
        return bool(user.email)

    def send(self, user: User, message: str, subject: str = "Уведомление") -> dict:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return {
                'success': True,
                'message': 'Email отправлен успешно'
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Ошибка отправки email: {str(e)}'
            }
