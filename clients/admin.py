from django.contrib import admin
from .models import Client, ClientContact

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'email', 'client_type', 'is_active', 'total_projects', 'created_at']
    list_filter = ['client_type', 'is_active', 'created_at']
    search_fields = ['name', 'company', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'total_projects', 'active_projects']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'client_type', 'is_active')
        }),
        ('Company Details', {
            'fields': ('company', 'website', 'address', 'contact_person')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('total_projects', 'active_projects', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ClientContact)
class ClientContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'email', 'position', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['name', 'email', 'client__name', 'client__company']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Contact Information', {
            'fields': ('client', 'name', 'email', 'phone', 'position', 'is_primary')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
