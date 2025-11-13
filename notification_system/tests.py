from django.test import TestCase
from django.contrib.auth.models import User
from notification_system.models import UserProfile
from notification_system.services.notification_service import NotificationService
from notification_system.services.providers.email_provider import EmailProvider
from notification_system.services.providers.sms_provider import SMSProvider


class NotificationTests(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            phone='+79123456789',
            telegram_chat_id='123456'
        )

    def test_email_provider_availability(self):
        """Тест доступности email провайдера"""
        provider = EmailProvider()
        self.assertTrue(provider.is_available(self.user))

    def test_sms_provider_availability(self):
        """Тест доступности SMS провайдера"""
        provider = SMSProvider(api_key='test-key')
        self.assertTrue(provider.is_available(self.user))

    def test_notification_service_initialization(self):
        """Тест инициализации сервиса уведомлений"""
        service = NotificationService()
        self.assertGreater(len(service.providers), 0)

    def test_send_notification_success(self):
        """Тест успешной отправки уведомления"""
        service = NotificationService()
        result = service.send_notification(
            user=self.user,
            message='Test message',
            subject='Test Subject'
        )
        self.assertTrue(result['success'])
