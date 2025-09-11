from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, validate_email
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

User = get_user_model()


class EventType(models.Model):
    """
    Types of events (Birthday, Anniversary, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True,
                            help_text="Font Awesome icon class")
    color = models.CharField(
        max_length=7, default='#3498db', help_text="Hex color code")
    default_message_template = models.TextField(blank=True)
    is_recurring = models.BooleanField(
        default=True, help_text="Does this event type repeat annually?")
    advance_notice_days = models.PositiveIntegerField(
        default=0, help_text="Days before event to send notifications")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_types'
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipient(models.Model):
    """
    People who will receive the flyers and messages
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipients')

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[validate_email])
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(
        max_length=20, blank=True, help_text="WhatsApp number (can be different from phone)")

    # Additional Details
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    anniversary_date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)

    # Contact Preferences
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('both', 'Both'),
    ], default='both')

    # Photos
    profile_photo = models.ImageField(
        upload_to='recipient_photos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['png', 'jpg', 'jpeg'])],
        help_text="Photo to use in flyers"
    )

    # Metadata
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    tags = models.CharField(max_length=200, blank=True,
                            help_text="Comma-separated tags")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recipients'
        verbose_name = _('Recipient')
        verbose_name_plural = _('Recipients')
        ordering = ['first_name', 'last_name']
        unique_together = ['owner', 'email']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    @property
    def next_birthday(self):
        """Get next birthday date"""
        if self.date_of_birth:
            today = timezone.now().date()
            next_birthday = self.date_of_birth.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return next_birthday
        return None

    @property
    def next_anniversary(self):
        """Get next anniversary date"""
        if self.anniversary_date:
            today = timezone.now().date()
            next_anniversary = self.anniversary_date.replace(year=today.year)
            if next_anniversary < today:
                next_anniversary = next_anniversary.replace(
                    year=today.year + 1)
            return next_anniversary
        return None


class ScheduledEvent(models.Model):
    """
    Events scheduled for automatic flyer generation and sending
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    RECURRENCE_TYPES = [
        ('once', 'One Time'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='scheduled_events')
    recipient = models.ForeignKey(
        Recipient, on_delete=models.CASCADE, related_name='events')
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)

    # Event Details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    event_time = models.TimeField(default='09:00:00')

    # Template and Customization
    template = models.ForeignKey(
        'templates.FlyerTemplate', on_delete=models.CASCADE, null=True, blank=True)
    custom_message = models.TextField(blank=True)
    custom_data = models.JSONField(
        default=dict, help_text="Additional data for template customization")

    # Scheduling
    recurrence_type = models.CharField(
        max_length=20, choices=RECURRENCE_TYPES, default='once')
    advance_send_days = models.PositiveIntegerField(
        default=0, help_text="Send notification X days before event")
    send_on_day = models.BooleanField(
        default=True, help_text="Send notification on the event day")

    # Notification Preferences
    send_email = models.BooleanField(default=True)
    send_whatsapp = models.BooleanField(default=True)
    email_subject = models.CharField(max_length=200, blank=True)
    email_body = models.TextField(blank=True)
    whatsapp_message = models.TextField(blank=True)

    # Status and Tracking
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    last_processed = models.DateTimeField(null=True, blank=True)
    next_execution = models.DateTimeField(null=True, blank=True)
    execution_count = models.PositiveIntegerField(default=0)

    # Generated Content
    generated_flyer = models.ImageField(
        upload_to='generated_flyers/', blank=True, null=True)
    generation_log = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'scheduled_events'
        verbose_name = _('Scheduled Event')
        verbose_name_plural = _('Scheduled Events')
        ordering = ['event_date', 'event_time']

    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()} on {self.event_date}"

    def calculate_next_execution(self):
        """Calculate when this event should next be executed"""
        if self.status in ['completed', 'cancelled']:
            return None

        event_datetime = timezone.make_aware(
            datetime.combine(self.event_date, self.event_time)
        )

        # If it's a one-time event and date has passed
        if self.recurrence_type == 'once' and event_datetime < timezone.now():
            return None

        # For advance notifications
        if self.advance_send_days > 0:
            advance_datetime = event_datetime - \
                timedelta(days=self.advance_send_days)
            if advance_datetime > timezone.now():
                return advance_datetime

        # For day-of notifications
        if self.send_on_day and event_datetime > timezone.now():
            return event_datetime

        # For yearly recurring events
        if self.recurrence_type == 'yearly' and event_datetime < timezone.now():
            next_year_datetime = event_datetime.replace(
                year=event_datetime.year + 1)
            return next_year_datetime

        return event_datetime

    def is_due_for_execution(self):
        """Check if this event is due for execution"""
        if not self.next_execution:
            return False
        return self.next_execution <= timezone.now()

    def mark_completed(self):
        """Mark event as completed and update next execution if recurring"""
        self.status = 'completed'
        self.last_processed = timezone.now()
        self.execution_count += 1

        if self.recurrence_type == 'yearly':
            self.next_execution = self.calculate_next_execution()
            self.status = 'pending'  # Reset for next year
        else:
            self.next_execution = None

        self.save()


class EventTemplate(models.Model):
    """
    Pre-defined event templates for quick setup
    """
    name = models.CharField(max_length=200)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    # Default settings
    default_title_template = models.CharField(
        max_length=200, help_text="Template for event title with placeholders")
    default_message = models.TextField()
    default_advance_days = models.PositiveIntegerField(default=0)
    default_send_on_day = models.BooleanField(default=True)

    # Associated flyer template
    suggested_template = models.ForeignKey(
        'templates.FlyerTemplate', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_templates'
        verbose_name = _('Event Template')
        verbose_name_plural = _('Event Templates')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.event_type.name})"


class BulkEventImport(models.Model):
    """
    Track bulk imports of events from CSV/Excel files
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bulk_imports')
    file = models.FileField(upload_to='bulk_imports/', validators=[
        FileExtensionValidator(allowed_extensions=['csv', 'xlsx', 'xls'])
    ])

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    total_rows = models.PositiveIntegerField(default=0)
    processed_rows = models.PositiveIntegerField(default=0)
    successful_imports = models.PositiveIntegerField(default=0)
    failed_imports = models.PositiveIntegerField(default=0)

    error_log = models.TextField(blank=True)
    import_summary = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bulk_event_imports'
        verbose_name = _('Bulk Event Import')
        verbose_name_plural = _('Bulk Event Imports')
        ordering = ['-created_at']

    def __str__(self):
        return f"Bulk import by {self.owner.get_full_name()} - {self.status}"
