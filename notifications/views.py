from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json

# Placeholder views - will be implemented later


class NotificationListView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/list.html'


class NotificationDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/detail.html'


class NotificationSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/settings.html'


class NotificationLogView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/log.html'


class NotificationAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/analytics.html'


class ChannelConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/channels.html'


class EmailConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/email_config.html'


class WhatsAppConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/whatsapp_config.html'


class SMSConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/sms_config.html'


class NotificationStatusView(LoginRequiredMixin, TemplateView):
    template_name = 'notifications/status.html'

# API-like placeholder views


def retry_notification(request, pk):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Notification queued for retry'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def resend_notification(request, pk):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Notification resent'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def test_notification(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Test notification sent'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def notification_stats(request):
    stats = {
        'total': 100,
        'sent': 85,
        'failed': 10,
        'pending': 5
    }
    return JsonResponse(stats)
