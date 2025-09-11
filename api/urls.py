"""
API URLs
"""
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Template API
    path('templates/', views.template_list_api, name='template_list'),
    path('templates/<int:pk>/', views.template_detail_api, name='template_detail'),
    path('templates/upload/', views.template_upload_api, name='template_upload'),

    # Event API
    path('events/', views.event_list_api, name='event_list'),
    path('events/<int:pk>/', views.event_detail_api, name='event_detail'),
    path('events/create/', views.event_create_api, name='event_create'),
    path('events/<int:pk>/execute/', views.event_execute_api, name='event_execute'),

    # Recipient API
    path('recipients/', views.recipient_list_api, name='recipient_list'),
    path('recipients/import/', views.recipient_import_api, name='recipient_import'),

    # Notification API
    path('notifications/stats/', views.notification_stats_api,
         name='notification_stats'),

    # Dashboard API
    path('dashboard/data/', views.dashboard_data_api, name='dashboard_data'),

    # Flyer generation
    path('generate-flyer/', views.generate_flyer_api, name='generate_flyer'),

    # Webhooks
    path('webhooks/', views.webhook_handler, name='webhook_handler'),
]
