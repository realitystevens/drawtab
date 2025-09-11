"""
Templates URLs
"""
from django.urls import path
from . import views

app_name = 'templates'

urlpatterns = [
    # Template listing and management
    path('', views.TemplateListView.as_view(), name='list'),
    path('my-templates/', views.MyTemplatesView.as_view(), name='my_templates'),
    path('public-templates/', views.PublicTemplatesView.as_view(),
         name='public_templates'),
    path('categories/', views.TemplateCategoryListView.as_view(), name='categories'),

    # Template CRUD
    path('upload/', views.TemplateUploadView.as_view(), name='upload'),
    path('<int:pk>/', views.TemplateDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TemplateEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TemplateDeleteView.as_view(), name='delete'),
    path('<int:pk>/clone/', views.TemplateCloneView.as_view(), name='clone'),

    # Dynamic areas management
    path('<int:template_id>/areas/',
         views.DynamicAreasView.as_view(), name='areas'),
    path('<int:template_id>/areas/add/',
         views.AddDynamicAreaView.as_view(), name='add_area'),
    path('areas/<int:pk>/edit/',
         views.EditDynamicAreaView.as_view(), name='edit_area'),
    path('areas/<int:pk>/delete/',
         views.DeleteDynamicAreaView.as_view(), name='delete_area'),

    # Template preview and testing
    path('<int:pk>/preview/', views.TemplatePreviewView.as_view(), name='preview'),
    path('<int:pk>/test/', views.TemplateTestView.as_view(), name='test'),

    # Rating and reviews
    path('<int:pk>/rate/', views.TemplateRatingView.as_view(), name='rate'),

    # Analytics
    path('<int:pk>/analytics/',
         views.TemplateAnalyticsView.as_view(), name='analytics'),
]
