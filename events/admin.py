from django.contrib import admin
from django.utils.html import format_html
from .models import (
    EventType, Recipient, ScheduledEvent, EventTemplate, BulkEventImport
)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_box', 'is_recurring',
                    'advance_notice_days', 'is_active', 'created_at')
    list_filter = ('is_recurring', 'is_active', 'created_at')
    search_fields = ('name', 'description')

    def color_box(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_box.short_description = 'Color'


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'owner',
                    'department', 'position', 'is_active', 'created_at')
    list_filter = ('gender', 'is_active', 'department',
                   'preferred_contact_method', 'created_at')
    search_fields = ('first_name', 'last_name', 'email',
                     'department', 'position', 'owner__email')
    readonly_fields = ('age', 'next_birthday',
                       'next_anniversary', 'created_at', 'updated_at')

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'anniversary_date')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number', 'whatsapp_number', 'preferred_contact_method')
        }),
        ('Work Information', {
            'fields': ('department', 'position')
        }),
        ('Media', {
            'fields': ('profile_photo',)
        }),
        ('Settings', {
            'fields': ('is_active', 'notes', 'tags')
        }),
        ('Computed Fields', {
            'fields': ('age', 'next_birthday', 'next_anniversary'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ScheduledEvent)
class ScheduledEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'event_type', 'event_date',
                    'status', 'next_execution', 'execution_count')
    list_filter = ('status', 'event_type', 'recurrence_type',
                   'send_email', 'send_whatsapp', 'created_at')
    search_fields = ('title', 'description', 'recipient__first_name',
                     'recipient__last_name', 'recipient__email')
    readonly_fields = ('id', 'next_execution', 'execution_count',
                       'last_processed', 'created_at', 'updated_at')
    date_hierarchy = 'event_date'

    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'event_type', 'event_date', 'event_time')
        }),
        ('Recipient & Template', {
            'fields': ('recipient', 'template', 'custom_message')
        }),
        ('Scheduling', {
            'fields': ('recurrence_type', 'advance_send_days', 'send_on_day')
        }),
        ('Notifications', {
            'fields': ('send_email', 'send_whatsapp', 'email_subject', 'email_body', 'whatsapp_message')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'next_execution', 'execution_count', 'last_processed')
        }),
        ('Generated Content', {
            'fields': ('generated_flyer', 'generation_log'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'default_advance_days',
                    'default_send_on_day', 'is_active', 'created_at')
    list_filter = ('event_type', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'default_title_template')


@admin.register(BulkEventImport)
class BulkEventImportAdmin(admin.ModelAdmin):
    list_display = ('owner', 'status', 'total_rows', 'successful_imports',
                    'failed_imports', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('owner__email', 'owner__first_name', 'owner__last_name')
    readonly_fields = ('total_rows', 'processed_rows', 'successful_imports',
                       'failed_imports', 'created_at', 'completed_at')

    fieldsets = (
        ('Import Information', {
            'fields': ('owner', 'file', 'status')
        }),
        ('Progress', {
            'fields': ('total_rows', 'processed_rows', 'successful_imports', 'failed_imports')
        }),
        ('Results', {
            'fields': ('error_log', 'import_summary'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )
