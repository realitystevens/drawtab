"""
Dashboard URLs
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('overview/', views.DashboardOverviewView.as_view(), name='overview'),
    path('stats/', views.DashboardStatsView.as_view(), name='stats'),
    path('widget/<int:widget_id>/data/',
         views.WidgetDataView.as_view(), name='widget_data'),
    path('settings/', views.DashboardSettingsView.as_view(), name='settings'),
    path('activity/', views.ActivityLogView.as_view(), name='activity'),
]
