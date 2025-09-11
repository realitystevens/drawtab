"""
Management command to initialize default data for DrawTab
"""
from django.core.management.base import BaseCommand
from templates.models import TemplateCategory
from events.models import EventType
from notifications.models import NotificationChannel
from dashboard.models import DashboardWidget


class Command(BaseCommand):
    help = 'Initialize default data for DrawTab application'

    def handle(self, *args, **options):
        self.stdout.write('Creating default data...')

        # Create template categories
        categories = [
            {'name': 'Birthday', 'description': 'Birthday celebration templates',
                'icon': 'fas fa-birthday-cake', 'color': '#e74c3c'},
            {'name': 'Anniversary', 'description': 'Anniversary celebration templates',
                'icon': 'fas fa-heart', 'color': '#e91e63'},
            {'name': 'Promotion', 'description': 'Job promotion and achievement templates',
                'icon': 'fas fa-trophy', 'color': '#f39c12'},
            {'name': 'Holiday', 'description': 'Holiday and seasonal templates',
                'icon': 'fas fa-gift', 'color': '#27ae60'},
            {'name': 'Welcome', 'description': 'Welcome and onboarding templates',
                'icon': 'fas fa-hands', 'color': '#3498db'},
            {'name': 'General', 'description': 'General purpose templates',
                'icon': 'fas fa-star', 'color': '#9b59b6'},
        ]

        for i, cat_data in enumerate(categories):
            category, created = TemplateCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'sort_order': i * 10
                }
            )
            if created:
                self.stdout.write(
                    f'Created template category: {category.name}')

        # Create event types
        event_types = [
            {
                'name': 'Birthday',
                'description': 'Employee birthday celebrations',
                'icon': 'fas fa-birthday-cake',
                'color': '#e74c3c',
                'default_message_template': 'Happy Birthday, {name}! 🎉 Wishing you a wonderful year ahead!',
                'is_recurring': True,
                'advance_notice_days': 0
            },
            {
                'name': 'Work Anniversary',
                'description': 'Work anniversary celebrations',
                'icon': 'fas fa-briefcase',
                'color': '#3498db',
                'default_message_template': 'Congratulations on your work anniversary, {name}! Thank you for your dedication and contributions.',
                'is_recurring': True,
                'advance_notice_days': 0
            },
            {
                'name': 'Wedding Anniversary',
                'description': 'Wedding anniversary celebrations',
                'icon': 'fas fa-heart',
                'color': '#e91e63',
                'default_message_template': 'Happy Anniversary, {name}! Wishing you many more years of happiness together.',
                'is_recurring': True,
                'advance_notice_days': 0
            },
            {
                'name': 'Promotion',
                'description': 'Job promotions and achievements',
                'icon': 'fas fa-trophy',
                'color': '#f39c12',
                'default_message_template': 'Congratulations on your promotion, {name}! Well deserved!',
                'is_recurring': False,
                'advance_notice_days': 0
            },
            {
                'name': 'New Hire Welcome',
                'description': 'Welcome messages for new employees',
                'icon': 'fas fa-user-plus',
                'color': '#27ae60',
                'default_message_template': 'Welcome to the team, {name}! We\'re excited to have you on board.',
                'is_recurring': False,
                'advance_notice_days': 0
            },
        ]

        for event_data in event_types:
            event_type, created = EventType.objects.get_or_create(
                name=event_data['name'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event type: {event_type.name}')

        # Create notification channels
        channels = [
            {
                'name': 'email',
                'display_name': 'Email',
                'description': 'Send notifications via email',
                'is_active': True,
                'requires_api_key': False,
                'configuration_fields': {
                    'smtp_host': 'SMTP Host',
                    'smtp_port': 'SMTP Port',
                    'smtp_username': 'SMTP Username',
                    'smtp_password': 'SMTP Password'
                },
                'rate_limit_per_minute': 10,
                'rate_limit_per_hour': 100,
                'rate_limit_per_day': 1000
            },
            {
                'name': 'whatsapp',
                'display_name': 'WhatsApp',
                'description': 'Send notifications via WhatsApp using Twilio',
                'is_active': True,
                'requires_api_key': True,
                'configuration_fields': {
                    'twilio_account_sid': 'Twilio Account SID',
                    'twilio_auth_token': 'Twilio Auth Token',
                    'twilio_phone_number': 'Twilio Phone Number'
                },
                'rate_limit_per_minute': 5,
                'rate_limit_per_hour': 50,
                'rate_limit_per_day': 200
            },
            {
                'name': 'sms',
                'display_name': 'SMS',
                'description': 'Send notifications via SMS using Twilio',
                'is_active': True,
                'requires_api_key': True,
                'configuration_fields': {
                    'twilio_account_sid': 'Twilio Account SID',
                    'twilio_auth_token': 'Twilio Auth Token',
                    'twilio_phone_number': 'Twilio Phone Number'
                },
                'rate_limit_per_minute': 5,
                'rate_limit_per_hour': 50,
                'rate_limit_per_day': 200
            }
        ]

        for channel_data in channels:
            channel, created = NotificationChannel.objects.get_or_create(
                name=channel_data['name'],
                defaults=channel_data
            )
            if created:
                self.stdout.write(
                    f'Created notification channel: {channel.display_name}')

        # Create dashboard widgets
        widgets = [
            {
                'name': 'Statistics Overview',
                'widget_type': 'stats_overview',
                'description': 'Overview of key statistics',
                'is_active': True,
                'default_configuration': {
                    'show_events': True,
                    'show_recipients': True,
                    'show_templates': True,
                    'show_notifications': True
                }
            },
            {
                'name': 'Upcoming Events',
                'widget_type': 'upcoming_events',
                'description': 'List of upcoming scheduled events',
                'is_active': True,
                'default_configuration': {
                    'max_items': 5,
                    'show_recipient': True,
                    'show_date': True
                }
            },
            {
                'name': 'Recent Activity',
                'widget_type': 'recent_activity',
                'description': 'Recent user activity log',
                'is_active': True,
                'default_configuration': {
                    'max_items': 10,
                    'show_timestamps': True
                }
            },
            {
                'name': 'Notification Status',
                'widget_type': 'notification_status',
                'description': 'Status of recent notifications',
                'is_active': True,
                'default_configuration': {
                    'period_days': 30,
                    'show_charts': True
                }
            },
            {
                'name': 'Template Usage',
                'widget_type': 'template_usage',
                'description': 'Template usage statistics',
                'is_active': True,
                'default_configuration': {
                    'show_most_used': True,
                    'max_items': 5
                }
            },
            {
                'name': 'Calendar View',
                'widget_type': 'calendar',
                'description': 'Calendar view of events',
                'is_active': True,
                'default_configuration': {
                    'view_type': 'month',
                    'show_event_types': True
                }
            }
        ]

        for widget_data in widgets:
            widget, created = DashboardWidget.objects.get_or_create(
                name=widget_data['name'],
                defaults=widget_data
            )
            if created:
                self.stdout.write(f'Created dashboard widget: {widget.name}')

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully initialized default data for DrawTab!')
        )
