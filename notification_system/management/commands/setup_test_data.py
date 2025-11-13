from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notification_system.models import UserProfile
from notification_system.services.notification_service import NotificationService
import random


class Command(BaseCommand):
    help = 'Создает тестовых пользователей и отправляет тестовые уведомления'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Количество тестовых пользователей для создания'
        )
        parser.add_argument(
            '--notifications',
            type=int,
            default=2,
            help='Количество тестовых уведомлений на пользователя'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие тестовые данные перед созданием'
        )

    def handle(self, *args, **options):
        users_count = options['users']
        notifications_count = options['notifications']
        clear_existing = options['clear']

        self.stdout.write(self.style.SUCCESS(
            f'🚀 Начинаем создание тестовых данных...'
        ))

        if clear_existing:
            self.clear_test_data()

        # Создаем тестовых пользователей
        test_users = self.create_test_users(users_count)

        # Отправляем тестовые уведомления
        self.send_test_notifications(test_users, notifications_count)

        self.stdout.write(self.style.SUCCESS(
            f'✅ Тестовые данные успешно созданы!'
        ))

    def clear_test_data(self):
        """Очистка существующих тестовых данных"""
        self.stdout.write('🧹 Очищаем существующие тестовые данные...')

        # Удаляем тестовых пользователей (имена начинаются с test_)
        test_users = User.objects.filter(username__startswith='test_')
        deleted_count, _ = test_users.delete()

        self.stdout.write(self.style.WARNING(
            f'🗑️ Удалено тестовых пользователей: {deleted_count}'
        ))

    def create_test_users(self, count):
        """Создание тестовых пользователей"""
        self.stdout.write(f'👥 Создаем {count} тестовых пользователей...')

        test_users = []

        for i in range(1, count + 1):
            username = f'test_user_{i}'
            email = f'test{i}@example.com'

            # Создаем пользователя
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': 'testpass123'
                }
            )

            # Определяем контакты пользователя (случайным образом)
            contacts = self.generate_user_contacts(i)

            # Создаем профиль
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults=contacts
            )

            # Обновляем контакты если профиль уже существовал
            if not profile_created:
                for key, value in contacts.items():
                    setattr(profile, key, value)
                profile.save()

            status = "создан" if created else "обновлен"
            self.stdout.write(
                f'   👤 {username} {status} - '
                f'Email: {user.email}, '
                f'Phone: {profile.phone or "нет"}, '
                f'Telegram: {profile.telegram_chat_id or "нет"}'
            )

            test_users.append(user)

        return test_users

    def generate_user_contacts(self, user_num):
        """Генерирует контакты пользователя с разными комбинациями"""
        contacts = {}

        # Разные комбинации контактов для тестирования
        if user_num % 3 == 1:
            # Только email
            contacts = {'phone': None, 'telegram_chat_id': None}
        elif user_num % 3 == 2:
            # Email + телефон
            contacts = {'phone': f'+791234567{user_num:02d}', 'telegram_chat_id': None}
        else:
            # Все контакты
            contacts = {
                'phone': f'+791234567{user_num:02d}',
                'telegram_chat_id': f'100000000{user_num}'
            }

        return contacts

    def send_test_notifications(self, users, count):
        """Отправка тестовых уведомлений"""
        self.stdout.write(f'📨 Отправляем {count} тестовых уведомлений на пользователя...')

        service = NotificationService()
        test_messages = [
            {
                'message': 'Добро пожаловать в нашу систему! 🎉',
                'subject': 'Приветственное письмо',
                'priority': 'low'
            },
            {
                'message': 'Ваш заказ №12345 готов к выдаче.',
                'subject': 'Статус заказа',
                'priority': 'medium'
            },
            {
                'message': '⚠️ СРОЧНО: Обнаружена подозрительная активность в вашем аккаунте!',
                'subject': 'ВАЖНО: Безопасность аккаунта',
                'priority': 'high'
            },
            {
                'message': 'Напоминаем о предстоящей встрече завтра в 15:00.',
                'subject': 'Напоминание о встрече',
                'priority': 'medium'
            },
            {
                'message': 'Спасибо за обратную связь! Мы ценим ваше мнение. 💫',
                'subject': 'Благодарность',
                'priority': 'low'
            }
        ]

        for user in users:
            self.stdout.write(f'\n🎯 Пользователь: {user.username}')

            for i in range(min(count, len(test_messages))):
                message_data = test_messages[i]

                # Разные стратегии отправки для тестирования
                if i == 0:
                    # Все каналы
                    preferred_channels = None
                elif i == 1:
                    # Только email
                    preferred_channels = ['email']
                else:
                    # Случайные каналы
                    channels = ['email', 'sms', 'telegram']
                    preferred_channels = random.sample(
                        channels,
                        random.randint(1, len(channels))
                    ) if random.random() > 0.3 else None

                # Отправка уведомления
                result = service.send_notification(
                    user=user,
                    message=message_data['message'],
                    subject=message_data['subject'],
                    priority=message_data['priority'],
                    preferred_channels=preferred_channels
                )

                # Вывод результата
                channels_info = "все каналы" if not preferred_channels else f"каналы: {preferred_channels}"
                status_style = self.style.SUCCESS if result['success'] else self.style.ERROR

                self.stdout.write(
                    f'   📧 Уведомление {i + 1} ({channels_info}): '
                    f'{status_style(result["channel_used"] or "none")} - '
                    f'{result["message"]}'
                )

    def show_statistics(self):
        """Показывает статистику после создания данных"""
        from notification_system.models import NotificationLog

        total_users = User.objects.count()
        total_profiles = UserProfile.objects.count()
        total_notifications = NotificationLog.objects.count()
        successful_notifications = NotificationLog.objects.filter(success=True).count()

        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('📊 СТАТИСТИКА СИСТЕМЫ:'))
        self.stdout.write(f'   👥 Всего пользователей: {total_users}')
        self.stdout.write(f'   📋 Профилей пользователей: {total_profiles}')
        self.stdout.write(f'   📨 Всего уведомлений: {total_notifications}')
        self.stdout.write(f'   ✅ Успешных отправок: {successful_notifications}')
        self.stdout.write(f'   ❌ Неуспешных отправок: {total_notifications - successful_notifications}')
        self.stdout.write('=' * 50)
