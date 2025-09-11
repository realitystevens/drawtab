"""
Events URLs
"""
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Event management
    path('', views.EventListView.as_view(), name='list'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.EventEditView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/duplicate/',
         views.EventDuplicateView.as_view(), name='duplicate'),

    # Event processing
    path('<uuid:pk>/execute/', views.ExecuteEventView.as_view(), name='execute'),
    path('<uuid:pk>/preview/', views.PreviewEventView.as_view(), name='preview'),

    # Recipients management
    path('recipients/', views.RecipientListView.as_view(), name='recipients'),
    path('recipients/create/', views.RecipientCreateView.as_view(),
         name='recipient_create'),
    path('recipients/<int:pk>/', views.RecipientDetailView.as_view(),
         name='recipient_detail'),
    path('recipients/<int:pk>/edit/',
         views.RecipientEditView.as_view(), name='recipient_edit'),
    path('recipients/<int:pk>/delete/',
         views.RecipientDeleteView.as_view(), name='recipient_delete'),
    path('recipients/import/', views.RecipientImportView.as_view(),
         name='recipient_import'),
    path('recipients/export/', views.RecipientExportView.as_view(),
         name='recipient_export'),

    # Bulk operations
    path('bulk/create/', views.BulkEventCreateView.as_view(), name='bulk_create'),
    path('bulk/import/', views.BulkEventImportView.as_view(), name='bulk_import'),
    path('bulk/import/<int:pk>/', views.BulkImportDetailView.as_view(),
         name='bulk_import_detail'),

    # Event types and templates
    path('types/', views.EventTypeListView.as_view(), name='types'),
    path('templates/', views.EventTemplateListView.as_view(), name='event_templates'),

    # Calendar and scheduling
    path('calendar/', views.EventCalendarView.as_view(), name='calendar'),
    path('upcoming/', views.UpcomingEventsView.as_view(), name='upcoming'),

    # Analytics
    path('analytics/', views.EventAnalyticsView.as_view(), name='analytics'),
]
