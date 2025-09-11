from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile, UserSettings


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:index')


class RegisterView(CreateView):
    model = CustomUser
    template_name = 'accounts/register.html'
    fields = ['email', 'first_name', 'last_name', 'password']
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Create user profile and settings
        UserProfile.objects.create(user=self.object)
        UserSettings.objects.create(user=self.object)
        messages.success(
            self.request, 'Account created successfully! Please log in.')
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'accounts/profile_edit.html'
    fields = ['first_name', 'last_name', 'company_name',
              'phone_number', 'profile_picture']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'


class EmailVerificationView(TemplateView):
    template_name = 'accounts/email_verification.html'


class ResendVerificationView(TemplateView):
    template_name = 'accounts/resend_verification.html'
