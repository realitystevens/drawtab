"""
Celery tasks for event processing
"""

from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from .models import ScheduledEvent, Recipient
from templates.models import FlyerTemplate
from templates.utils import FlyerGenerator
from notifications.models import NotificationQueue, NotificationChannel
import logging
from datetime import datetime, timedelta

User = get_user_model()
logger = logging.getLogger(__name__)


@shared_task
def process_scheduled_events():
    """
    Process events that are due for execution
    """
    try:
        # Get events that are due for processing
        due_events = ScheduledEvent.objects.filter(
            status='pending',
            next_execution__lte=timezone.now()
        ).select_related('recipient', 'event_type', 'template', 'owner')

        processed_count = 0
        for event in due_events:
            try:
                # Generate flyer
                if event.template:
                    flyer_file = generate_event_flyer.delay(
                        str(event.id)).get()
                    if flyer_file:
                        event.generated_flyer.save(
                            f'flyer_{event.id}.jpg',
                            ContentFile(flyer_file),
                            save=False
                        )

                # Queue notifications
                queue_event_notifications.delay(str(event.id))

                # Mark as completed
                event.mark_completed()
                processed_count += 1

                logger.info(
                    f"Processed event: {event.title} for {event.recipient.get_full_name()}")

            except Exception as e:
                event.status = 'failed'
                event.generation_log = f"Error: {str(e)}"
                event.save(update_fields=['status', 'generation_log'])
                logger.error(f"Error processing event {event.id}: {str(e)}")

        logger.info(f"Processed {processed_count} scheduled events")
        return processed_count

    except Exception as e:
        logger.error(f"Error in process_scheduled_events: {str(e)}")
        return 0


@shared_task
def generate_event_flyer(event_id):
    """
    Generate flyer for a specific event
    """
    try:
        event = ScheduledEvent.objects.get(id=event_id)

        if not event.template:
            logger.warning(f"No template for event {event_id}")
            return None

        # Prepare recipient data
        recipient_data = {
            'first_name': event.recipient.first_name,
            'last_name': event.recipient.last_name,
            'photo_path': event.recipient.profile_photo.name if event.recipient.profile_photo else None,
            'custom_message': event.custom_message or event.event_type.default_message_template,
            'event_date': event.event_date,
        }

        # Add custom data
        recipient_data.update(event.custom_data or {})

        # Get dynamic areas from template
        dynamic_areas = []
        for area in event.template.areas.all():
            dynamic_areas.append({
                'area_type': area.area_type,
                'x_position': area.x_position,
                'y_position': area.y_position,
                'width': area.width,
                'height': area.height,
                'font_family': area.font_family,
                'font_size': area.font_size,
                'font_color': area.font_color,
                'font_weight': area.font_weight,
                'text_align': area.text_align,
                'border_radius': area.border_radius,
                'border_width': area.border_width,
                'border_color': area.border_color,
                'default_text': getattr(area, 'default_text', ''),
                'data_key': getattr(area, 'data_key', ''),
            })

        # Generate flyer
        generator = FlyerGenerator()
        flyer_file = generator.generate_flyer(
            event.template.image_file.name,
            dynamic_areas,
            recipient_data
        )

        if flyer_file:
            # Update template usage
            event.template.increment_usage()

            # Log the generation
            from templates.models import TemplateUsageLog
            TemplateUsageLog.objects.create(
                template=event.template,
                user=event.owner,
                event_type=event.event_type.name
            )

            return flyer_file.read()

        return None

    except Exception as e:
        logger.error(f"Error generating flyer for event {event_id}: {str(e)}")
        return None


@shared_task
def queue_event_notifications(event_id):
    """
    Queue notifications for an event
    """
    try:
        event = ScheduledEvent.objects.select_related(
            'recipient', 'owner', 'event_type'
        ).get(id=event_id)

        # Get notification channels
        email_channel = NotificationChannel.objects.filter(
            name='email').first()
        whatsapp_channel = NotificationChannel.objects.filter(
            name='whatsapp').first()

        notifications_queued = 0

        # Queue email notification
        if event.send_email and email_channel and event.recipient.email:
            email_subject = event.email_subject or f"{event.event_type.name} - {event.recipient.get_full_name()}"
            email_body = event.email_body or event.custom_message or event.event_type.default_message_template

            NotificationQueue.objects.create(
                user=event.owner,
                scheduled_event=event,
                channel=email_channel,
                recipient_email=event.recipient.email,
                recipient_name=event.recipient.get_full_name(),
                subject=email_subject,
                message=email_body,
                scheduled_for=timezone.now(),
                attachments=[
                    event.generated_flyer.name] if event.generated_flyer else []
            )
            notifications_queued += 1

        # Queue WhatsApp notification
        if event.send_whatsapp and whatsapp_channel and event.recipient.whatsapp_number:
            whatsapp_message = event.whatsapp_message or event.custom_message or event.event_type.default_message_template

            NotificationQueue.objects.create(
                user=event.owner,
                scheduled_event=event,
                channel=whatsapp_channel,
                recipient_phone=event.recipient.whatsapp_number,
                recipient_name=event.recipient.get_full_name(),
                message=whatsapp_message,
                scheduled_for=timezone.now(),
                attachments=[
                    event.generated_flyer.name] if event.generated_flyer else []
            )
            notifications_queued += 1

        logger.info(
            f"Queued {notifications_queued} notifications for event {event_id}")
        return notifications_queued

    except Exception as e:
        logger.error(
            f"Error queuing notifications for event {event_id}: {str(e)}")
        return 0


@shared_task
def bulk_create_events(user_id, recipients_data, event_data):
    """
    Create multiple events in bulk
    """
    try:
        user = User.objects.get(id=user_id)
        created_count = 0
        errors = []

        for recipient_data in recipients_data:
            try:
                # Create or get recipient
                recipient, created = Recipient.objects.get_or_create(
                    owner=user,
                    email=recipient_data['email'],
                    defaults={
                        'first_name': recipient_data.get('first_name', ''),
                        'last_name': recipient_data.get('last_name', ''),
                        'phone_number': recipient_data.get('phone_number', ''),
                        'whatsapp_number': recipient_data.get('whatsapp_number', ''),
                        'department': recipient_data.get('department', ''),
                        'position': recipient_data.get('position', ''),
                        'date_of_birth': recipient_data.get('date_of_birth'),
                        'anniversary_date': recipient_data.get('anniversary_date'),
                    }
                )

                # Create scheduled event
                scheduled_event = ScheduledEvent.objects.create(
                    owner=user,
                    recipient=recipient,
                    **event_data
                )

                # Calculate next execution
                scheduled_event.next_execution = scheduled_event.calculate_next_execution()
                scheduled_event.save(update_fields=['next_execution'])

                created_count += 1

            except Exception as e:
                errors.append(
                    f"Error creating event for {recipient_data.get('email', 'unknown')}: {str(e)}")

        logger.info(f"Bulk created {created_count} events for user {user_id}")
        return {
            'created_count': created_count,
            'errors': errors
        }

    except Exception as e:
        logger.error(f"Error in bulk_create_events: {str(e)}")
        return {
            'created_count': 0,
            'errors': [str(e)]
        }


@shared_task
def calculate_next_executions():
    """
    Recalculate next execution times for all pending events
    """
    try:
        events = ScheduledEvent.objects.filter(status='pending')
        updated_count = 0

        for event in events:
            old_execution = event.next_execution
            new_execution = event.calculate_next_execution()

            if old_execution != new_execution:
                event.next_execution = new_execution
                event.save(update_fields=['next_execution'])
                updated_count += 1

        logger.info(f"Updated {updated_count} event execution times")
        return updated_count

    except Exception as e:
        logger.error(f"Error calculating next executions: {str(e)}")
        return 0
