"""
DrawTab URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/', include('accounts.urls')),

    # Main application URLs
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('dashboard/', include('dashboard.urls')),
    path('templates/', include('templates.urls')),
    path('events/', include('events.urls')),
    path('notifications/', include('notifications.urls')),

    # API endpoints
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "DrawTab Administration"
admin.site.site_title = "DrawTab Admin"
admin.site.index_title = "Welcome to DrawTab Administration"
