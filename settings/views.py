from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import UserSetting
from .forms import UserSettingForm
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import UserSettingSerializer


@login_required
def profile_settings(request):
    """View for handling profile settings"""
    user = request.user
    
    if request.method == 'POST':
        # Placeholder for form handling
        # In a real implementation, you would create and validate a form
        messages.success(request, _("Profile settings updated successfully"))
        return redirect('settings:profile')
    
    # Create an empty form context to prevent template errors
    form = {'display_name': {'value': ''}, 'avatar': {'errors': []}, 'location': {'value': ''}, 'bio': {'value': ''}, 'website': {'value': ''}}
    
    return render(request, 'settings/profile.html', {
        'active_tab': 'profile',
        'form': form
    })


@login_required
def account_settings(request):
    """View for handling account settings"""
    user = request.user
    
    return render(request, 'settings/account.html', {
        'active_tab': 'account'
    })


@login_required
def privacy_settings(request):
    """View for handling privacy settings"""
    user = request.user
    
    if request.method == 'POST':
        # Placeholder for form handling
        # In a real implementation, you would create and validate a form
        messages.success(request, _("Privacy settings updated successfully"))
        return redirect('settings:privacy')
    
    return render(request, 'settings/privacy.html', {
        'active_tab': 'privacy'
    })


@login_required
def notification_settings(request):
    """View for handling notification settings"""
    user = request.user
    
    if request.method == 'POST':
        # Placeholder for form handling
        # In a real implementation, you would create and validate a form
        messages.success(request, _("Notification settings updated successfully"))
        return redirect('settings:notifications')
    
    return render(request, 'settings/notifications.html', {
        'active_tab': 'notifications'
    })


@login_required
def settings_view(request):
    """View for displaying and updating user settings"""
    user_settings, created = UserSetting.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserSettingForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your settings have been updated successfully.')
            return redirect('settings:settings_view')
    else:
        form = UserSettingForm(instance=user_settings)
    
    context = {
        'form': form,
        'user_settings': user_settings,
    }
    
    return render(request, 'settings/settings.html', context)


class UserSettingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user settings to be viewed or edited.
    """
    serializer_class = UserSettingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        This view returns settings for the currently authenticated user only.
        """
        return UserSetting.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Associate the current user with new settings.
        """
        serializer.save(user=self.request.user)
        
    def retrieve(self, request, *args, **kwargs):
        """
        Get user settings or create default settings if none exist.
        """
        try:
            instance = UserSetting.objects.get(user=request.user)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except UserSetting.DoesNotExist:
            # Create default settings for this user
            instance = UserSetting.objects.create(user=request.user)
            serializer = self.get_serializer(instance)
            return Response(serializer.data) 