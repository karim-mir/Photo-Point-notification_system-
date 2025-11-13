from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from notification_system.models import NotificationChannel


class BaseNotificationProvider(ABC):

    def __init__(self):
        self.channel_type = None

    @abstractmethod
    def send(self, user: User, message: str, subject: str = None) -> dict:
        pass

    @abstractmethod
    def is_available(self, user: User) -> bool:
        pass

    def get_priority(self) -> int:
        priorities = {
            NotificationChannel.EMAIL: 1,
            NotificationChannel.TELEGRAM: 2,
            NotificationChannel.SMS: 3
        }
        return priorities.get(self.channel_type, 99)
