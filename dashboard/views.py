from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta

from events.models import ScheduledEvent, Recipient
from templates.models import FlyerTemplate
from notifications.models import NotificationLog
from .models import UserDashboard, ActivityLog


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get or create user dashboard
        dashboard, created = UserDashboard.objects.get_or_create(user=user)
        if created:
            dashboard.update_stats()

        # Basic stats
        context.update({
            'total_events': ScheduledEvent.objects.filter(owner=user).count(),
            'total_recipients': Recipient.objects.filter(owner=user).count(),
            'total_templates': FlyerTemplate.objects.filter(owner=user).count(),
            'total_notifications_sent': NotificationLog.objects.filter(user=user).count(),
        })

        # Upcoming events
        upcoming_events = ScheduledEvent.objects.filter(
            owner=user,
            event_date__gte=timezone.now().date(),
            status='pending'
        ).order_by('event_date')[:5]
        context['upcoming_events'] = upcoming_events

        # Recent activity
        recent_activity = ActivityLog.objects.filter(
            user=user
        ).order_by('-created_at')[:10]
        context['recent_activity'] = recent_activity

        # This month's stats
        now = timezone.now()
        month_start = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

        context.update({
            'events_this_month': ScheduledEvent.objects.filter(
                owner=user,
                created_at__gte=month_start
            ).count(),
            'notifications_this_month': NotificationLog.objects.filter(
                user=user,
                sent_at__gte=month_start
            ).count(),
        })

        return context


class DashboardOverviewView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Comprehensive stats
        context['stats'] = {
            'events': {
                'total': ScheduledEvent.objects.filter(owner=user).count(),
                'pending': ScheduledEvent.objects.filter(owner=user, status='pending').count(),
                'completed': ScheduledEvent.objects.filter(owner=user, status='completed').count(),
                'failed': ScheduledEvent.objects.filter(owner=user, status='failed').count(),
            },
            'recipients': {
                'total': Recipient.objects.filter(owner=user).count(),
                'active': Recipient.objects.filter(owner=user, is_active=True).count(),
            },
            'templates': {
                'total': FlyerTemplate.objects.filter(owner=user).count(),
                'public': FlyerTemplate.objects.filter(owner=user, is_public=True).count(),
            },
            'notifications': {
                'total': NotificationLog.objects.filter(user=user).count(),
                'delivered': NotificationLog.objects.filter(user=user, status='delivered').count(),
                'failed': NotificationLog.objects.filter(user=user, status='failed').count(),
            }
        }

        return context


class DashboardStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/stats.html'


class WidgetDataView(LoginRequiredMixin, TemplateView):
    def get(self, request, widget_id):
        # Return JSON data for dashboard widgets
        return JsonResponse({'data': 'widget_data'})


class DashboardSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/settings.html'


class ActivityLogView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        activities = ActivityLog.objects.filter(
            user=self.request.user
        ).order_by('-created_at')[:50]

        context['activities'] = activities
        return context
