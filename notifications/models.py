from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid

User = get_user_model()


class NotificationChannel(models.Model):
    """
    Available notification channels (Email, WhatsApp, SMS, etc.)
    """
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    requires_api_key = models.BooleanField(default=False)
    configuration_fields = models.JSONField(
        default=dict, help_text="Required configuration fields")

    # Rate limiting
    rate_limit_per_minute = models.PositiveIntegerField(default=10)
    rate_limit_per_hour = models.PositiveIntegerField(default=100)
    rate_limit_per_day = models.PositiveIntegerField(default=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_channels'
        verbose_name = _('Notification Channel')
        verbose_name_plural = _('Notification Channels')
        ordering = ['name']

    def __str__(self):
        return self.display_name


class NotificationTemplate(models.Model):
    """
    Templates for different types of notifications
    """
    TEMPLATE_TYPES = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('promotion', 'Promotion'),
        ('holiday', 'Holiday'),
        ('reminder', 'Reminder'),
        ('custom', 'Custom'),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_templates')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)

    # Content
    subject_template = models.CharField(
        max_length=200, blank=True, help_text="For email notifications")
    body_template = models.TextField(
        help_text="Template with placeholders like {name}, {event_date}, etc.")

    # Template variables
    available_variables = models.JSONField(
        default=list, help_text="List of available placeholder variables")

    # Settings
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_templates'
        verbose_name = _('Notification Template')
        verbose_name_plural = _('Notification Templates')
        ordering = ['template_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.channel.display_name})"


class NotificationQueue(models.Model):
    """
    Queue for notifications to be sent
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('retry', 'Retry'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationship
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_queue')
    scheduled_event = models.ForeignKey(
        'events.ScheduledEvent', on_delete=models.CASCADE, null=True, blank=True)
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)

    # Recipient
    recipient_email = models.EmailField(blank=True)
    recipient_phone = models.CharField(max_length=20, blank=True)
    recipient_name = models.CharField(max_length=200)

    # Content
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    attachments = models.JSONField(
        default=list, help_text="List of file paths to attach")

    # Scheduling
    scheduled_for = models.DateTimeField(default=timezone.now)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='normal')

    # Status and Tracking
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)

    # Response tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    # Error handling
    error_message = models.TextField(blank=True)
    retry_after = models.DateTimeField(null=True, blank=True)

    # Metadata
    metadata = models.JSONField(
        default=dict, help_text="Additional data for the notification")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_queue'
        verbose_name = _('Notification Queue')
        verbose_name_plural = _('Notification Queue')
        ordering = ['priority', 'scheduled_for']
        indexes = [
            models.Index(fields=['status', 'scheduled_for']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['channel', 'status']),
        ]

    def __str__(self):
        return f"{self.channel.display_name} to {self.recipient_name} - {self.status}"

    def mark_sent(self):
        """Mark notification as sent"""
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at'])

    def mark_failed(self, error_message=''):
        """Mark notification as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.attempts += 1

        # Schedule retry if not exceeded max attempts
        if self.attempts < self.max_attempts:
            self.status = 'retry'
            self.retry_after = timezone.now() + timezone.timedelta(
                minutes=5 * (2 ** self.attempts)  # Exponential backoff
            )

        self.save(update_fields=[
                  'status', 'error_message', 'attempts', 'retry_after'])

    def can_retry(self):
        """Check if notification can be retried"""
        return (
            self.status == 'retry' and
            self.attempts < self.max_attempts and
            self.retry_after and
            self.retry_after <= timezone.now()
        )


class NotificationLog(models.Model):
    """
    Log of all sent notifications for tracking and analytics
    """
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
        ('spam', 'Marked as Spam'),
    ]

    notification_queue = models.OneToOneField(
        NotificationQueue,
        on_delete=models.CASCADE,
        related_name='log'
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_logs')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)

    # Recipient info (copied from queue)
    recipient_email = models.EmailField(blank=True)
    recipient_phone = models.CharField(max_length=20, blank=True)
    recipient_name = models.CharField(max_length=200)

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    # Timestamps
    sent_at = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    # Analytics
    click_count = models.PositiveIntegerField(default=0)
    bounce_reason = models.CharField(max_length=200, blank=True)

    # External service data
    external_id = models.CharField(
        max_length=100, blank=True, help_text="ID from external service (Twilio, etc.)")
    external_status = models.CharField(max_length=50, blank=True)

    # Costs (if applicable)
    cost = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_logs'
        verbose_name = _('Notification Log')
        verbose_name_plural = _('Notification Logs')
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['user', 'sent_at']),
            models.Index(fields=['channel', 'status']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return f"{self.channel.display_name} to {self.recipient_name} - {self.status}"


class UserNotificationSettings(models.Model):
    """
    User-specific notification settings and preferences
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='notification_settings')

    # Channel preferences
    email_enabled = models.BooleanField(default=True)
    whatsapp_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)

    # Timing preferences
    preferred_send_time = models.TimeField(default='09:00:00')
    timezone = models.CharField(max_length=50, default='UTC')

    # Rate limiting (user-specific)
    max_daily_notifications = models.PositiveIntegerField(default=50)
    max_hourly_notifications = models.PositiveIntegerField(default=10)

    # API credentials (encrypted)
    twilio_account_sid = models.CharField(max_length=200, blank=True)
    twilio_auth_token = models.CharField(max_length=200, blank=True)
    twilio_phone_number = models.CharField(max_length=20, blank=True)

    # Email settings
    custom_smtp_host = models.CharField(max_length=100, blank=True)
    custom_smtp_port = models.PositiveIntegerField(null=True, blank=True)
    custom_smtp_username = models.CharField(max_length=100, blank=True)
    custom_smtp_password = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_notification_settings'
        verbose_name = _('User Notification Settings')
        verbose_name_plural = _('User Notification Settings')

    def __str__(self):
        return f"Notification settings for {self.user.get_full_name()}"


class NotificationAnalytics(models.Model):
    """
    Daily analytics summary for notifications
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_analytics')
    date = models.DateField()

    # Counts by channel
    email_sent = models.PositiveIntegerField(default=0)
    email_delivered = models.PositiveIntegerField(default=0)
    email_read = models.PositiveIntegerField(default=0)
    email_failed = models.PositiveIntegerField(default=0)

    whatsapp_sent = models.PositiveIntegerField(default=0)
    whatsapp_delivered = models.PositiveIntegerField(default=0)
    whatsapp_read = models.PositiveIntegerField(default=0)
    whatsapp_failed = models.PositiveIntegerField(default=0)

    sms_sent = models.PositiveIntegerField(default=0)
    sms_delivered = models.PositiveIntegerField(default=0)
    sms_failed = models.PositiveIntegerField(default=0)

    # Costs
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    currency = models.CharField(max_length=3, default='USD')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_analytics'
        verbose_name = _('Notification Analytics')
        verbose_name_plural = _('Notification Analytics')
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"Analytics for {self.user.get_full_name()} on {self.date}"
