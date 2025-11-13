from django.contrib.auth.models import User
from .base import BaseNotificationProvider
from notification_system.models import NotificationChannel
import requests


class SMSProvider(BaseNotificationProvider):

    def __init__(self, api_key: str):
        super().__init__()
        self.channel_type = NotificationChannel.SMS
        self.api_key = api_key

    def is_available(self, user: User) -> bool:
        try:
            profile = user.userprofile
            return bool(profile.phone)
        except UserProfile.DoesNotExist:
            return False

    def send(self, user: User, message: str, subject: str = None) -> dict:
        try:
            profile = user.userprofile

            # Имитация отправки SMS через внешний API
            # response = requests.post(
            #     "https://sms-provider.com/api/send",
            #     json={"phone": profile.phone, "message": message},
            #     headers={"Authorization": f"Bearer {self.api_key}"}
            # )

            print(f"📱 SMS отправлено на {profile.phone}: {message}")

            return {
                'success': True,
                'message': 'SMS отправлено успешно'
            }

        except UserProfile.DoesNotExist:
            return {
                'success': False,
                'message': 'Профиль пользователя не найден'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Ошибка отправки SMS: {str(e)}'
            }
