from django.contrib import admin
from .models import CompanySettings, SystemSettings, UserPermission, SystemLog

@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'updated_at']
    search_fields = ['name', 'email']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'description', 'email', 'phone', 'address', 'website')
        }),
        ('Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url', 'github_url')
        }),
        ('Business Details', {
            'fields': ('tax_id', 'registration_number')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'session_timeout', 'max_login_attempts', 'api_rate_limit', 'updated_at']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Email Configuration', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'smtp_use_tls')
        }),
        ('Backup Settings', {
            'fields': ('auto_backup_enabled', 'backup_frequency')
        }),
        ('Security Settings', {
            'fields': ('session_timeout', 'max_login_attempts', 'password_expiry_days')
        }),
        ('API Settings', {
            'fields': ('api_rate_limit',)
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission', 'granted', 'granted_by', 'created_at']
    list_filter = ['permission', 'granted', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'granted_by')

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['level', 'message_short', 'module', 'user', 'created_at']
    list_filter = ['level', 'module', 'created_at']
    search_fields = ['message', 'module', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def message_short(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_short.short_description = 'Message'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
