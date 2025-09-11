from django.contrib import admin
from .models import WebsiteContent, BlogPost, PortfolioProject, Service, TeamMember

@admin.register(WebsiteContent)
class WebsiteContentAdmin(admin.ModelAdmin):
    list_display = ['section', 'title', 'is_active', 'updated_at']
    list_filter = ['section', 'is_active', 'updated_at']
    search_fields = ['title', 'content', 'section']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'category', 'published_at', 'created_at']
    list_filter = ['status', 'author', 'category', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'order', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'status', 'order', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'status', 'order', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'role', 'bio']
    readonly_fields = ['created_at', 'updated_at']
