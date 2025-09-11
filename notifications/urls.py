"""
Notifications URLs
"""
from django.urls import path
from . import views

app_name = 'notifications'

"""
Notifications URLs
"""

app_name = 'notifications'

urlpatterns = [
    # Notification management
    path('', views.NotificationListView.as_view(), name='list'),
    path('logs/', views.NotificationLogView.as_view(), name='logs'),
    path('analytics/', views.NotificationAnalyticsView.as_view(), name='analytics'),
    path('status/', views.NotificationStatusView.as_view(), name='status'),

    # Settings
    path('settings/', views.NotificationSettingsView.as_view(), name='settings'),
    path('channels/', views.ChannelConfigView.as_view(), name='channels'),
    path('email-config/', views.EmailConfigView.as_view(), name='email_config'),
    path('whatsapp-config/', views.WhatsAppConfigView.as_view(),
         name='whatsapp_config'),
    path('sms-config/', views.SMSConfigView.as_view(), name='sms_config'),

    # Notification actions
    path('<int:pk>/retry/', views.retry_notification, name='retry'),
    path('<int:pk>/resend/', views.resend_notification, name='resend'),
    path('test/', views.test_notification, name='test'),
    path('stats/', views.notification_stats, name='stats'),
]
