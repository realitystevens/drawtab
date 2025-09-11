"""
Celery tasks for notification processing
"""

from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import (
    NotificationQueue, NotificationLog, NotificationChannel,
    NotificationAnalytics, UserNotificationSettings
)
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import logging
from datetime import datetime, timedelta
import requests

User = get_user_model()
logger = logging.getLogger(__name__)


@shared_task
def process_notification_queue():
    """
    Process pending notifications in the queue
    """
    try:
        # Get notifications ready to be sent
        notifications = NotificationQueue.objects.filter(
            status='pending',
            scheduled_for__lte=timezone.now()
        ).select_related('channel', 'user')[:50]  # Process 50 at a time

        processed_count = 0
        for notification in notifications:
            try:
                # Mark as processing
                notification.status = 'processing'
                notification.save(update_fields=['status'])

                # Send based on channel
                if notification.channel.name == 'email':
                    send_email_notification.delay(str(notification.id))
                elif notification.channel.name == 'whatsapp':
                    send_whatsapp_notification.delay(str(notification.id))

                processed_count += 1

            except Exception as e:
                notification.mark_failed(str(e))
                logger.error(
                    f"Error processing notification {notification.id}: {str(e)}")

        # Process retry notifications
        retry_notifications = NotificationQueue.objects.filter(
            status='retry',
            retry_after__lte=timezone.now()
        ).select_related('channel', 'user')[:25]

        for notification in retry_notifications:
            try:
                notification.status = 'processing'
                notification.save(update_fields=['status'])

                if notification.channel.name == 'email':
                    send_email_notification.delay(str(notification.id))
                elif notification.channel.name == 'whatsapp':
                    send_whatsapp_notification.delay(str(notification.id))

                processed_count += 1

            except Exception as e:
                notification.mark_failed(str(e))

        logger.info(f"Processed {processed_count} notifications")
        return processed_count

    except Exception as e:
        logger.error(f"Error in process_notification_queue: {str(e)}")
        return 0


@shared_task
def send_email_notification(notification_id):
    """
    Send email notification
    """
    try:
        notification = NotificationQueue.objects.get(id=notification_id)

        # Prepare email
        email = EmailMessage(
            subject=notification.subject,
            body=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[notification.recipient_email],
        )

        # Add attachments
        for attachment_path in notification.attachments:
            try:
                from django.core.files.storage import default_storage
                if default_storage.exists(attachment_path):
                    with default_storage.open(attachment_path, 'rb') as f:
                        email.attach(
                            attachment_path.split('/')[-1],
                            f.read(),
                            'image/jpeg'
                        )
            except Exception as e:
                logger.warning(
                    f"Could not attach file {attachment_path}: {str(e)}")

        # Send email
        email.send()

        # Mark as sent
        notification.mark_sent()

        # Create log entry
        log_entry = NotificationLog.objects.create(
            notification_queue=notification,
            user=notification.user,
            channel=notification.channel,
            recipient_email=notification.recipient_email,
            recipient_name=notification.recipient_name,
            status='sent',
            sent_at=timezone.now()
        )

        logger.info(f"Email sent to {notification.recipient_email}")
        return True

    except Exception as e:
        try:
            notification = NotificationQueue.objects.get(id=notification_id)
            notification.mark_failed(str(e))
        except:
            pass
        logger.error(
            f"Error sending email notification {notification_id}: {str(e)}")
        return False


@shared_task
def send_whatsapp_notification(notification_id):
    """
    Send WhatsApp notification using Twilio
    """
    try:
        notification = NotificationQueue.objects.get(id=notification_id)

        # Get Twilio credentials
        user_settings = UserNotificationSettings.objects.filter(
            user=notification.user).first()

        if user_settings and user_settings.twilio_account_sid and user_settings.twilio_auth_token:
            account_sid = user_settings.twilio_account_sid
            auth_token = user_settings.twilio_auth_token
            from_number = user_settings.twilio_phone_number
        else:
            # Use global settings
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            from_number = settings.TWILIO_WHATSAPP_NUMBER

        if not all([account_sid, auth_token, from_number]):
            raise ValueError("Twilio credentials not configured")

        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Format phone number
        to_number = notification.recipient_phone
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'

        # Send message
        message = client.messages.create(
            body=notification.message,
            from_=from_number,
            to=to_number
        )

        # Mark as sent
        notification.mark_sent()

        # Create log entry
        log_entry = NotificationLog.objects.create(
            notification_queue=notification,
            user=notification.user,
            channel=notification.channel,
            recipient_phone=notification.recipient_phone,
            recipient_name=notification.recipient_name,
            status='sent',
            sent_at=timezone.now(),
            external_id=message.sid
        )

        logger.info(f"WhatsApp message sent to {notification.recipient_phone}")
        return True

    except TwilioException as e:
        try:
            notification = NotificationQueue.objects.get(id=notification_id)
            notification.mark_failed(f"Twilio error: {str(e)}")
        except:
            pass
        logger.error(
            f"Twilio error sending WhatsApp notification {notification_id}: {str(e)}")
        return False

    except Exception as e:
        try:
            notification = NotificationQueue.objects.get(id=notification_id)
            notification.mark_failed(str(e))
        except:
            pass
        logger.error(
            f"Error sending WhatsApp notification {notification_id}: {str(e)}")
        return False


@shared_task
def cleanup_old_notifications():
    """
    Clean up old notification logs and queue entries
    """
    try:
        # Delete old queue entries (completed/failed older than 30 days)
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted_queue = NotificationQueue.objects.filter(
            status__in=['sent', 'failed', 'cancelled'],
            created_at__lt=cutoff_date
        ).delete()

        # Delete old logs (older than 90 days)
        cutoff_date = timezone.now() - timedelta(days=90)
        deleted_logs = NotificationLog.objects.filter(
            sent_at__lt=cutoff_date
        ).delete()

        logger.info(
            f"Cleaned up {deleted_queue[0]} queue entries and {deleted_logs[0]} log entries")
        return {
            'queue_deleted': deleted_queue[0],
            'logs_deleted': deleted_logs[0]
        }

    except Exception as e:
        logger.error(f"Error in cleanup_old_notifications: {str(e)}")
        return {'error': str(e)}


@shared_task
def update_notification_analytics():
    """
    Update daily notification analytics
    """
    try:
        today = timezone.now().date()

        # Get all users who sent notifications today
        users_with_activity = NotificationLog.objects.filter(
            sent_at__date=today
        ).values_list('user_id', flat=True).distinct()

        updated_count = 0
        for user_id in users_with_activity:
            try:
                user = User.objects.get(id=user_id)

                # Get or create analytics record
                analytics, created = NotificationAnalytics.objects.get_or_create(
                    user=user,
                    date=today,
                    defaults={'total_cost': 0}
                )

                # Calculate counts
                logs = NotificationLog.objects.filter(
                    user=user,
                    sent_at__date=today
                )

                # Email stats
                email_logs = logs.filter(channel__name='email')
                analytics.email_sent = email_logs.count()
                analytics.email_delivered = email_logs.filter(
                    status='delivered').count()
                analytics.email_read = email_logs.filter(status='read').count()
                analytics.email_failed = email_logs.filter(
                    status='failed').count()

                # WhatsApp stats
                whatsapp_logs = logs.filter(channel__name='whatsapp')
                analytics.whatsapp_sent = whatsapp_logs.count()
                analytics.whatsapp_delivered = whatsapp_logs.filter(
                    status='delivered').count()
                analytics.whatsapp_read = whatsapp_logs.filter(
                    status='read').count()
                analytics.whatsapp_failed = whatsapp_logs.filter(
                    status='failed').count()

                # SMS stats
                sms_logs = logs.filter(channel__name='sms')
                analytics.sms_sent = sms_logs.count()
                analytics.sms_delivered = sms_logs.filter(
                    status='delivered').count()
                analytics.sms_failed = sms_logs.filter(status='failed').count()

                # Calculate total cost
                total_cost = logs.aggregate(
                    total=models.Sum('cost')
                )['total'] or 0
                analytics.total_cost = total_cost

                analytics.save()
                updated_count += 1

            except Exception as e:
                logger.error(
                    f"Error updating analytics for user {user_id}: {str(e)}")

        logger.info(f"Updated analytics for {updated_count} users")
        return updated_count

    except Exception as e:
        logger.error(f"Error in update_notification_analytics: {str(e)}")
        return 0


@shared_task
def send_bulk_notifications(user_id, notification_data_list):
    """
    Send multiple notifications in bulk
    """
    try:
        user = User.objects.get(id=user_id)
        channel = NotificationChannel.objects.get(
            name=notification_data_list[0]['channel'])

        created_count = 0
        for notification_data in notification_data_list:
            try:
                notification = NotificationQueue.objects.create(
                    user=user,
                    channel=channel,
                    recipient_email=notification_data.get(
                        'recipient_email', ''),
                    recipient_phone=notification_data.get(
                        'recipient_phone', ''),
                    recipient_name=notification_data.get('recipient_name', ''),
                    subject=notification_data.get('subject', ''),
                    message=notification_data.get('message', ''),
                    scheduled_for=timezone.now(),
                    attachments=notification_data.get('attachments', [])
                )
                created_count += 1

            except Exception as e:
                logger.error(f"Error creating bulk notification: {str(e)}")

        logger.info(
            f"Created {created_count} bulk notifications for user {user_id}")
        return created_count

    except Exception as e:
        logger.error(f"Error in send_bulk_notifications: {str(e)}")
        return 0


@shared_task
def check_delivery_status():
    """
    Check delivery status for sent notifications using external APIs
    """
    try:
        # Check notifications sent in last 24 hours that haven't been confirmed delivered
        cutoff_time = timezone.now() - timedelta(hours=24)

        logs_to_check = NotificationLog.objects.filter(
            sent_at__gte=cutoff_time,
            status='sent',
            external_id__isnull=False
        ).select_related('channel')

        updated_count = 0
        for log in logs_to_check:
            try:
                if log.channel.name == 'whatsapp' and log.external_id:
                    # Check Twilio status
                    status = check_twilio_message_status(
                        log.external_id, log.user)
                    if status and status != log.status:
                        log.status = status
                        if status == 'delivered':
                            log.delivered_at = timezone.now()
                        log.save(update_fields=['status', 'delivered_at'])
                        updated_count += 1

            except Exception as e:
                logger.error(
                    f"Error checking status for log {log.id}: {str(e)}")

        logger.info(f"Updated status for {updated_count} notification logs")
        return updated_count

    except Exception as e:
        logger.error(f"Error in check_delivery_status: {str(e)}")
        return 0


def check_twilio_message_status(message_sid, user):
    """
    Check message status from Twilio
    """
    try:
        user_settings = UserNotificationSettings.objects.filter(
            user=user).first()

        if user_settings and user_settings.twilio_account_sid and user_settings.twilio_auth_token:
            account_sid = user_settings.twilio_account_sid
            auth_token = user_settings.twilio_auth_token
        else:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN

        client = Client(account_sid, auth_token)
        message = client.messages(message_sid).fetch()

        # Map Twilio status to our status
        status_map = {
            'delivered': 'delivered',
            'read': 'read',
            'failed': 'failed',
            'undelivered': 'failed',
        }

        return status_map.get(message.status, 'sent')

    except Exception as e:
        logger.error(
            f"Error checking Twilio status for {message_sid}: {str(e)}")
        return None
