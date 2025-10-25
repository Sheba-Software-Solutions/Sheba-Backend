from django.contrib import admin
from .models import JobPosting, JobApplication

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'job_type', 'location', 'status', 'views', 'applications_count', 'created_at']
    list_filter = ['status', 'department', 'job_type', 'experience_level', 'created_at']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'applications_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'department', 'location', 'job_type', 'experience_level', 'status')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'responsibilities', 'benefits')
        }),
        ('Salary Information', {
            'fields': ('salary_min', 'salary_max', 'salary_currency', 'salary_display')
        }),
        ('Application Details', {
            'fields': ('application_deadline', 'application_email', 'application_url')
        }),
        ('Metadata', {
            'fields': ('posted_by', 'views', 'applications_count', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'job', 'email', 'years_of_experience', 'status', 'submitted_at']
    list_filter = ['status', 'job__department', 'years_of_experience', 'submitted_at']
    search_fields = ['first_name', 'last_name', 'email', 'job__title']
    readonly_fields = ['submitted_at', 'updated_at']
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Job Application', {
            'fields': ('job', 'cover_letter', 'resume', 'portfolio_url', 'linkedin_url')
        }),
        ('Experience', {
            'fields': ('years_of_experience', 'current_position', 'current_company')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )