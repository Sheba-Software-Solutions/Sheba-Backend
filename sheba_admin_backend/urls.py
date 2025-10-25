"""
URL configuration for sheba_admin_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/content/', include('content.urls')),
    path('api/communication/', include('communication.urls')),
    path('api/careers/', include('careers.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/settings/', include('settings_app.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
