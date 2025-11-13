from django.contrib.auth.models import User
from notification_system.models import NotificationChannel, NotificationLog, NotificationPriority
from .providers.email_provider import EmailProvider
from .providers.sms_provider import SMSProvider
from .providers.telegram_provider import TelegramProvider
from django.conf import settings


class NotificationService:

    def __init__(self):
        self.providers = []
        self._setup_providers()
        self.max_retries = 3

    def _setup_providers(self):
        """Инициализация провайдеров уведомлений"""
        self.providers.append(EmailProvider())

        if hasattr(settings, 'SMS_API_KEY') and settings.SMS_API_KEY:
            self.providers.append(SMSProvider(api_key=settings.SMS_API_KEY))

        if hasattr(settings, 'TELEGRAM_BOT_TOKEN') and settings.TELEGRAM_BOT_TOKEN:
            self.providers.append(TelegramProvider(bot_token=settings.TELEGRAM_BOT_TOKEN))

    def _get_available_channels(self, user: User, preferred_channels=None):
        """Получить доступные каналы для пользователя"""
        available_providers = []

        for provider in self.providers:
            if provider.is_available(user):
                available_providers.append(provider)

        # Сортировка по приоритету
        available_providers.sort(key=lambda p: p.get_priority())

        # Фильтрация по предпочтительным каналам
        if preferred_channels:
            available_providers = [p for p in available_providers if p.channel_type in preferred_channels]

        return available_providers

    def send_notification(self, user: User, message: str, subject: str = None,
                          priority: str = NotificationPriority.MEDIUM,
                          preferred_channels: list = None) -> dict:
        """Основной метод отправки уведомления"""

        available_channels = self._get_available_channels(user, preferred_channels)

        if not available_channels:
            # Логируем неудачную попытку
            NotificationLog.objects.create(
                user=user,
                message=message,
                subject=subject,
                channel_used=NotificationChannel.EMAIL,  # fallback
                priority=priority,
                success=False,
                error_message="Нет доступных каналов для отправки уведомления",
                retry_attempts=0
            )
            return {
                'success': False,
                'message': 'Нет доступных каналов для отправки уведомления'
            }

        last_error = None
        retry_attempts = 0

        for attempt in range(self.max_retries):
            for channel in available_channels:
                try:
                    print(f"🔄 Попытка {attempt + 1}: отправка через {channel.channel_type}")

                    result = channel.send(user, message, subject)

                    if result['success']:
                        # Логируем успешную отправку
                        NotificationLog.objects.create(
                            user=user,
                            message=message,
                            subject=subject,
                            channel_used=channel.channel_type,
                            priority=priority,
                            success=True,
                            retry_attempts=retry_attempts
                        )

                        return {
                            'success': True,
                            'channel_used': channel.channel_type,
                            'message': result['message'],
                            'retry_attempts': retry_attempts
                        }
                    else:
                        last_error = result['message']
                        retry_attempts += 1

                except Exception as e:
                    last_error = str(e)
                    retry_attempts += 1
                    continue

        # Логируем окончательную неудачу
        NotificationLog.objects.create(
            user=user,
            message=message,
            subject=subject,
            channel_used=available_channels[0].channel_type if available_channels else NotificationChannel.EMAIL,
            priority=priority,
            success=False,
            error_message=last_error,
            retry_attempts=retry_attempts
        )

        return {
            'success': False,
            'channel_used': None,
            'message': f'Все каналы недоступны. Последняя ошибка: {last_error}',
            'retry_attempts': retry_attempts
        }
