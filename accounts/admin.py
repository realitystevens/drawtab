from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile, UserSettings


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'company_name', 'is_premium', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_premium',
                   'email_verified', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'company_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
         'company_name', 'phone_number', 'profile_picture', 'timezone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Subscription'), {'fields': ('is_premium',
         'subscription_start', 'subscription_end')}),
        (_('Email verification'), {
         'fields': ('email_verified', 'email_verification_token')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'email_notifications',
                    'whatsapp_notifications', 'total_events_created', 'total_flyers_generated')
    list_filter = ('email_notifications',
                   'whatsapp_notifications', 'created_at')
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'location')
    readonly_fields = ('total_events_created', 'total_flyers_generated',
                       'total_messages_sent', 'created_at', 'updated_at')


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'auto_schedule_enabled',
                    'bulk_processing_enabled', 'analytics_enabled')
    list_filter = ('auto_schedule_enabled',
                   'bulk_processing_enabled', 'analytics_enabled')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
