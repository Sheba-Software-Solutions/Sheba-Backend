from django.contrib import admin
from .models import Project, ProjectTask

class ProjectTaskInline(admin.TabularInline):
    model = ProjectTask
    extra = 0
    fields = ['title', 'assigned_to', 'status', 'due_date', 'estimated_hours', 'actual_hours']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'status', 'priority', 'progress', 'start_date', 'end_date']
    list_filter = ['status', 'priority', 'client', 'start_date']
    search_fields = ['name', 'description', 'client__name']
    filter_horizontal = ['assigned_to']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProjectTaskInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'client')
        }),
        ('Project Details', {
            'fields': ('status', 'priority', 'assigned_to', 'progress')
        }),
        ('Timeline & Budget', {
            'fields': ('start_date', 'end_date', 'budget')
        }),
        ('Technical Details', {
            'fields': ('technologies', 'repository_url', 'live_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'status', 'due_date', 'estimated_hours', 'actual_hours']
    list_filter = ['status', 'project', 'assigned_to', 'due_date']
    search_fields = ['title', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Task Information', {
            'fields': ('project', 'title', 'description')
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status', 'due_date')
        }),
        ('Time Tracking', {
            'fields': ('estimated_hours', 'actual_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
