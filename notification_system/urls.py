from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_notification, name='send_notification'),
    path('history/<int:user_id>/', views.notification_history, name='notification_history'),
    path('channels/<int:user_id>/', views.user_channels, name='user_channels'),
]
