from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    # Company Settings
    path('company/', views.CompanySettingsView.as_view(), name='company-settings'),
    
    # System Settings
    path('system/', views.SystemSettingsView.as_view(), name='system-settings'),
    path('system/health/', views.system_health, name='system-health'),
    path('system/backup/', views.backup_database, name='backup-database'),
    path('system/restore/', views.restore_database, name='restore-database'),
    
    # User Permissions
    path('permissions/', views.UserPermissionListCreateView.as_view(), name='permission-list-create'),
    path('permissions/<int:pk>/', views.UserPermissionDetailView.as_view(), name='permission-detail'),
    path('users/<int:user_id>/permissions/', views.user_permissions, name='user-permissions'),
    
    # System Logs
    path('logs/', views.SystemLogListView.as_view(), name='log-list'),
    path('logs/<int:pk>/', views.SystemLogDetailView.as_view(), name='log-detail'),
]
