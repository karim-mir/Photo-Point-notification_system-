# 🔔 Система Уведомлений (Notification System)
Django-сервис для надежной отправки уведомлений пользователям через multiple каналы с автоматическим fallback механизмом.

## 🚀 Возможности
- 📧 Email уведомления - через Django email backend

- 📱 SMS уведомления - интеграция с SMS провайдерами

- 📲 Telegram уведомления - отправка через Telegram Bot API

- 🔄 Автоматический fallback - при ошибке в одном канале автоматически пробует другие

- 📊 Логирование - полная история отправки уведомлений

- 🎯 Приоритизация - умный выбор каналов отправки

- ⚡ Retry логика - до 3 попыток отправки

- 🔧 Гибкая конфигурация - легко добавлять новые провайдеры

## 🏗️ Архитектура
```commandline
notification_system/
├── notification_system/
│   ├── models.py                      # Модели UserProfile, NotificationLog
│   ├── services/
│   │   ├── notification_service.py    # Основной сервис
│   │   └── providers/                 # Провайдеры уведомлений
│   │       ├── base.py                # Базовый класс провайдера
│   │       ├── email_provider.py
│   │       ├── sms_provider.py
│   │       └── telegram_provider.py
│   ├── views.py                       # API endpoints
│   └── admin.py                       # Django admin
└── config/
    └── settings.py                    # Настройки Django
```
## ⚙️ Установка и настройка
### 1. Клонирование и установка зависимостей
```commandline
git clone <https://github.com/karim-mir/Photo-Point-notification_system->
```
### 2. Настройка базы данных
````commandline
# Применение миграций
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
````
### 3. Конфигурация провайдеров
```commandline
# Email настройки
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'

# SMS провайдер
SMS_API_KEY = 'your-sms-api-key'

# Telegram провайдер
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
```
### 4. Запуск сервера
```commandline
python manage.py runserver
```
## 📡 API Endpoints
### Отправка уведомления
POST /api/notifications/send/
```commandline
{
  "user_id": 1,
  "message": "Ваш заказ готов к выдаче",
  "subject": "Статус заказа", 
  "priority": "high",
  "preferred_channels": ["email", "telegram"]
}
```