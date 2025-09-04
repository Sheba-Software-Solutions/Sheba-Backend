from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanySettings(models.Model):
    """Company information and settings"""
    name = models.CharField(max_length=200, default="Sheba Software")
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    favicon = models.ImageField(upload_to='company/', blank=True, null=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Business Details
    tax_id = models.CharField(max_length=50, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Company Settings"
        verbose_name_plural = "Company Settings"
    
    def __str__(self):
        return self.name

class SystemSettings(models.Model):
    """System-wide settings and configurations"""
    # Email Settings
    smtp_host = models.CharField(max_length=100, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=100, blank=True)
    smtp_password = models.CharField(max_length=100, blank=True)
    smtp_use_tls = models.BooleanField(default=True)
    
    # Backup Settings
    auto_backup_enabled = models.BooleanField(default=False)
    backup_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        default='weekly'
    )
    
    # Security Settings
    session_timeout = models.IntegerField(default=30, help_text="Session timeout in minutes")
    max_login_attempts = models.IntegerField(default=5)
    password_expiry_days = models.IntegerField(default=90)
    
    # API Settings
    api_rate_limit = models.IntegerField(default=1000, help_text="Requests per hour")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "System Settings"
        verbose_name_plural = "System Settings"
    
    def __str__(self):
        return "System Settings"

class UserPermission(models.Model):
    """Custom user permissions for role-based access"""
    PERMISSION_TYPES = [
        ('dashboard.view', 'View Dashboard'),
        ('projects.view', 'View Projects'),
        ('projects.add', 'Add Projects'),
        ('projects.change', 'Edit Projects'),
        ('projects.delete', 'Delete Projects'),
        ('clients.view', 'View Clients'),
        ('clients.add', 'Add Clients'),
        ('clients.change', 'Edit Clients'),
        ('clients.delete', 'Delete Clients'),
        ('content.view', 'View Content'),
        ('content.add', 'Add Content'),
        ('content.change', 'Edit Content'),
        ('content.delete', 'Delete Content'),
        ('communication.view', 'View Communication'),
        ('communication.add', 'Add Communication'),
        ('communication.change', 'Edit Communication'),
        ('communication.delete', 'Delete Communication'),
        ('settings.view', 'View Settings'),
        ('settings.change', 'Edit Settings'),
        ('users.view', 'View Users'),
        ('users.add', 'Add Users'),
        ('users.change', 'Edit Users'),
        ('users.delete', 'Delete Users'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_permissions')
    permission = models.CharField(max_length=50, choices=PERMISSION_TYPES)
    granted = models.BooleanField(default=True)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='granted_permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'permission']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_permission_display()}"

class SystemLog(models.Model):
    """System logs for monitoring and debugging"""
    LOG_LEVELS = [
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    level = models.CharField(max_length=20, choices=LOG_LEVELS)
    message = models.TextField()
    module = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.level.upper()}: {self.message[:50]}..."
