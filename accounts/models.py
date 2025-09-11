from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User model with additional fields for the DrawTab application
    """
    email = models.EmailField(_('email address'), unique=True)
    company_name = models.CharField(
        max_length=200, blank=True, null=True, help_text="Company or organization name")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    is_premium = models.BooleanField(
        default=False, help_text="Premium subscription status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(
        max_length=100, blank=True, null=True)

    # Subscription details
    subscription_start = models.DateTimeField(blank=True, null=True)
    subscription_end = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'custom_users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    @property
    def is_subscription_active(self):
        """Check if user has an active subscription"""
        if not self.is_premium or not self.subscription_end:
            return False
        from django.utils import timezone
        return timezone.now() <= self.subscription_end


class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=True)
    notification_time = models.TimeField(
        default='09:00:00', help_text="Preferred time to receive notifications")

    # Usage statistics
    total_events_created = models.PositiveIntegerField(default=0)
    total_flyers_generated = models.PositiveIntegerField(default=0)
    total_messages_sent = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"


class UserSettings(models.Model):
    """
    User-specific application settings
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='settings')

    # Default template preferences
    default_template_category = models.CharField(max_length=50, blank=True)
    auto_schedule_enabled = models.BooleanField(default=True)

    # Messaging preferences
    default_email_template = models.TextField(
        blank=True, help_text="Default email message template")
    default_whatsapp_template = models.TextField(
        blank=True, help_text="Default WhatsApp message template")

    # Advanced settings
    bulk_processing_enabled = models.BooleanField(default=False)
    analytics_enabled = models.BooleanField(default=True)
    data_retention_days = models.PositiveIntegerField(default=365)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_settings'
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')

    def __str__(self):
        return f"Settings for {self.user.get_full_name()}"
