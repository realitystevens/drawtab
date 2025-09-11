from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Placeholder views - will be implemented later


class TemplateListView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/list.html'


class MyTemplatesView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/my_templates.html'


class PublicTemplatesView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/public_templates.html'


class TemplateCategoryListView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/categories.html'


class TemplateUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/upload.html'


class TemplateDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/detail.html'


class TemplateEditView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/edit.html'


class TemplateDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/delete.html'


class TemplateCloneView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/clone.html'


class DynamicAreasView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/areas.html'


class AddDynamicAreaView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/add_area.html'


class EditDynamicAreaView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/edit_area.html'


class DeleteDynamicAreaView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/delete_area.html'


class TemplatePreviewView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/preview.html'


class TemplateTestView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/test.html'


class TemplateRatingView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/rate.html'


class TemplateAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'templates/analytics.html'
