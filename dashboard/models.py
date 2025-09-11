from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


class DashboardWidget(models.Model):
    """
    Dashboard widgets that users can add to their dashboard
    """
    WIDGET_TYPES = [
        ('stats_overview', 'Statistics Overview'),
        ('upcoming_events', 'Upcoming Events'),
        ('recent_activity', 'Recent Activity'),
        ('notification_status', 'Notification Status'),
        ('template_usage', 'Template Usage'),
        ('cost_summary', 'Cost Summary'),
        ('quick_actions', 'Quick Actions'),
        ('calendar', 'Calendar View'),
    ]

    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    default_configuration = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dashboard_widgets'
        verbose_name = _('Dashboard Widget')
        verbose_name_plural = _('Dashboard Widgets')
        ordering = ['name']

    def __str__(self):
        return self.name


class UserDashboard(models.Model):
    """
    User's personalized dashboard configuration
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='dashboard')
    layout = models.JSONField(
        default=dict, help_text="Dashboard layout configuration")
    theme = models.CharField(max_length=20, default='light', choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ])

    # Quick stats cache (updated periodically)
    total_events = models.PositiveIntegerField(default=0)
    total_recipients = models.PositiveIntegerField(default=0)
    total_templates = models.PositiveIntegerField(default=0)
    total_notifications_sent = models.PositiveIntegerField(default=0)

    # Activity summary
    events_this_month = models.PositiveIntegerField(default=0)
    notifications_this_month = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)

    # Settings
    show_welcome_message = models.BooleanField(default=True)
    auto_refresh_interval = models.PositiveIntegerField(
        default=30, help_text="Auto-refresh interval in seconds")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_dashboards'
        verbose_name = _('User Dashboard')
        verbose_name_plural = _('User Dashboards')

    def __str__(self):
        return f"Dashboard for {self.user.get_full_name()}"

    def update_stats(self):
        """Update dashboard statistics"""
        from events.models import ScheduledEvent, Recipient
        from templates.models import FlyerTemplate
        from notifications.models import NotificationLog

        self.total_events = ScheduledEvent.objects.filter(
            owner=self.user).count()
        self.total_recipients = Recipient.objects.filter(
            owner=self.user).count()
        self.total_templates = FlyerTemplate.objects.filter(
            owner=self.user).count()
        self.total_notifications_sent = NotificationLog.objects.filter(
            user=self.user).count()

        # This month's activity
        now = timezone.now()
        month_start = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

        self.events_this_month = ScheduledEvent.objects.filter(
            owner=self.user,
            created_at__gte=month_start
        ).count()

        self.notifications_this_month = NotificationLog.objects.filter(
            user=self.user,
            sent_at__gte=month_start
        ).count()

        self.last_activity = now
        self.save()


class UserDashboardWidget(models.Model):
    """
    User's dashboard widget instances with their configurations
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='dashboard_widgets')
    widget = models.ForeignKey(DashboardWidget, on_delete=models.CASCADE)

    # Position and size
    position_x = models.PositiveIntegerField(default=0)
    position_y = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=4)  # Grid units
    height = models.PositiveIntegerField(default=3)  # Grid units

    # Configuration
    configuration = models.JSONField(default=dict)
    is_visible = models.BooleanField(default=True)

    # Data caching
    cached_data = models.JSONField(default=dict)
    cache_updated_at = models.DateTimeField(null=True, blank=True)
    cache_ttl = models.PositiveIntegerField(
        default=300, help_text="Cache TTL in seconds")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_dashboard_widgets'
        verbose_name = _('User Dashboard Widget')
        verbose_name_plural = _('User Dashboard Widgets')
        unique_together = ['user', 'widget']
        ordering = ['position_y', 'position_x']

    def __str__(self):
        return f"{self.widget.name} for {self.user.get_full_name()}"

    def is_cache_valid(self):
        """Check if cached data is still valid"""
        if not self.cache_updated_at:
            return False
        return (timezone.now() - self.cache_updated_at).total_seconds() < self.cache_ttl

    def get_widget_data(self):
        """Get widget data (from cache or generate new)"""
        if self.is_cache_valid():
            return self.cached_data

        # Generate new data based on widget type
        data = self._generate_widget_data()

        # Update cache
        self.cached_data = data
        self.cache_updated_at = timezone.now()
        self.save(update_fields=['cached_data', 'cache_updated_at'])

        return data

    def _generate_widget_data(self):
        """Generate widget data based on widget type"""
        from events.models import ScheduledEvent, Recipient
        from templates.models import FlyerTemplate
        from notifications.models import NotificationLog

        widget_type = self.widget.widget_type

        if widget_type == 'stats_overview':
            return {
                'total_events': ScheduledEvent.objects.filter(owner=self.user).count(),
                'total_recipients': Recipient.objects.filter(owner=self.user).count(),
                'total_templates': FlyerTemplate.objects.filter(owner=self.user).count(),
                'notifications_sent': NotificationLog.objects.filter(user=self.user).count(),
            }

        elif widget_type == 'upcoming_events':
            upcoming = ScheduledEvent.objects.filter(
                owner=self.user,
                event_date__gte=timezone.now().date(),
                status='pending'
            ).order_by('event_date')[:5]

            return {
                'events': [
                    {
                        'id': str(event.id),
                        'title': event.title,
                        'recipient': event.recipient.get_full_name(),
                        'date': event.event_date.isoformat(),
                        'type': event.event_type.name,
                    }
                    for event in upcoming
                ]
            }

        elif widget_type == 'recent_activity':
            recent_logs = NotificationLog.objects.filter(
                user=self.user
            ).order_by('-sent_at')[:10]

            return {
                'activities': [
                    {
                        'id': log.id,
                        'action': f"Sent {log.channel.display_name}",
                        'recipient': log.recipient_name,
                        'timestamp': log.sent_at.isoformat(),
                        'status': log.status,
                    }
                    for log in recent_logs
                ]
            }

        elif widget_type == 'notification_status':
            # Last 30 days notification summary
            thirty_days_ago = timezone.now() - timedelta(days=30)
            logs = NotificationLog.objects.filter(
                user=self.user,
                sent_at__gte=thirty_days_ago
            )

            status_counts = {}
            for log in logs:
                status_counts[log.status] = status_counts.get(
                    log.status, 0) + 1

            return {
                'summary': status_counts,
                'total': logs.count(),
                'period': '30 days'
            }

        # Default empty data
        return {}


class ActivityLog(models.Model):
    """
    User activity log for dashboard and analytics
    """
    ACTION_TYPES = [
        ('login', 'User Login'),
        ('template_upload', 'Template Upload'),
        ('template_edit', 'Template Edit'),
        ('event_create', 'Event Create'),
        ('event_edit', 'Event Edit'),
        ('recipient_add', 'Recipient Add'),
        ('recipient_edit', 'Recipient Edit'),
        ('notification_send', 'Notification Send'),
        ('bulk_import', 'Bulk Import'),
        ('settings_change', 'Settings Change'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='activity_logs')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    description = models.CharField(max_length=200)

    # Related objects (optional)
    object_type = models.CharField(max_length=50, blank=True)
    object_id = models.CharField(max_length=100, blank=True)

    # Additional data
    metadata = models.JSONField(default=dict)

    # Request info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activity_logs'
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_action_type_display()}"


class SystemAlert(models.Model):
    """
    System-wide alerts and notifications for users
    """
    ALERT_TYPES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success'),
        ('maintenance', 'Maintenance'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    alert_type = models.CharField(
        max_length=20, choices=ALERT_TYPES, default='info')

    # Targeting
    target_all_users = models.BooleanField(default=True)
    target_users = models.ManyToManyField(
        User, blank=True, related_name='system_alerts')

    # Display settings
    is_active = models.BooleanField(default=True)
    is_dismissible = models.BooleanField(default=True)
    auto_dismiss_after = models.PositiveIntegerField(
        null=True, blank=True, help_text="Auto-dismiss after X seconds")

    # Scheduling
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_alerts')

    class Meta:
        db_table = 'system_alerts'
        verbose_name = _('System Alert')
        verbose_name_plural = _('System Alerts')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_visible_for_user(self, user):
        """Check if alert should be visible for a specific user"""
        if not self.is_active:
            return False

        now = timezone.now()
        if now < self.start_date or (self.end_date and now > self.end_date):
            return False

        if self.target_all_users:
            return True

        return self.target_users.filter(id=user.id).exists()


class UserAlertDismissal(models.Model):
    """
    Track which alerts users have dismissed
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='dismissed_alerts')
    alert = models.ForeignKey(
        SystemAlert, on_delete=models.CASCADE, related_name='dismissals')
    dismissed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_alert_dismissals'
        verbose_name = _('User Alert Dismissal')
        verbose_name_plural = _('User Alert Dismissals')
        unique_together = ['user', 'alert']

    def __str__(self):
        return f"{self.user.get_full_name()} dismissed {self.alert.title}"
