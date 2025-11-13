from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import NotificationLog
from .services.notification_service import NotificationService
import json


@api_view(['POST'])
def send_notification(request):
    """API endpoint для отправки уведомления"""

    user_id = request.data.get('user_id')
    message = request.data.get('message')
    subject = request.data.get('subject')
    priority = request.data.get('priority', 'medium')
    preferred_channels = request.data.get('preferred_channels')

    if not user_id or not message:
        return Response(
            {'error': 'user_id и message обязательны'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'Пользователь не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Отправка уведомления
    service = NotificationService()
    result = service.send_notification(
        user=user,
        message=message,
        subject=subject,
        priority=priority,
        preferred_channels=preferred_channels
    )

    if result['success']:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def notification_history(request, user_id):
    """История уведомлений пользователя"""
    user = get_object_or_404(User, id=user_id)
    notifications = NotificationLog.objects.filter(user=user).order_by('-created_at')[:50]

    data = []
    for notification in notifications:
        data.append({
            'id': notification.id,
            'message': notification.message,
            'subject': notification.subject,
            'channel_used': notification.channel_used,
            'priority': notification.priority,
            'success': notification.success,
            'created_at': notification.created_at.isoformat(),
            'retry_attempts': notification.retry_attempts
        })

    return Response({'notifications': data})


@api_view(['GET'])
def user_channels(request, user_id):
    """Доступные каналы для пользователя"""
    user = get_object_or_404(User, id=user_id)
    service = NotificationService()

    available_channels = []
    for provider in service.providers:
        if provider.is_available(user):
            available_channels.append(provider.channel_type)

    return Response({'available_channels': available_channels})
