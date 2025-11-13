from django.contrib.auth.models import User
from .base import BaseNotificationProvider
from notification_system.models import NotificationChannel
import requests


class TelegramProvider(BaseNotificationProvider):

    def __init__(self, bot_token: str):
        super().__init__()
        self.channel_type = NotificationChannel.TELEGRAM
        self.bot_token = bot_token

    def is_available(self, user: User) -> bool:
        try:
            profile = user.userprofile
            return bool(profile.telegram_chat_id)
        except UserProfile.DoesNotExist:
            return False

    def send(self, user: User, message: str, subject: str = None) -> dict:
        try:
            profile = user.userprofile

            # Имитация отправки Telegram сообщения
            full_message = f"{subject}\n\n{message}" if subject else message

            # В реальном проекте:
            # response = requests.post(
            #     f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            #     json={
            #         "chat_id": profile.telegram_chat_id,
            #         "text": full_message
            #     }
            # )

            print(f"📲 Telegram отправлен для {user.username}: {message}")

            return {
                'success': True,
                'message': 'Telegram сообщение отправлено успешно'
            }

        except UserProfile.DoesNotExist:
            return {
                'success': False,
                'message': 'Профиль пользователя не найден'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Ошибка отправки Telegram: {str(e)}'
            }
