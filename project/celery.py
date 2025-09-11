"""
Celery configuration for DrawTab application
"""

import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('drawtab')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'process-scheduled-events': {
        'task': 'events.tasks.process_scheduled_events',
        'schedule': 60.0,  # Run every minute
    },
    'send-notification-queue': {
        'task': 'notifications.tasks.process_notification_queue',
        'schedule': 30.0,  # Run every 30 seconds
    },
    'cleanup-old-notifications': {
        'task': 'notifications.tasks.cleanup_old_notifications',
        'schedule': 86400.0,  # Run daily
    },
    'update-dashboard-stats': {
        'task': 'dashboard.tasks.update_user_dashboard_stats',
        'schedule': 3600.0,  # Run hourly
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
