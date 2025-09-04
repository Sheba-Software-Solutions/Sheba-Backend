from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardMetric(models.Model):
    """Dashboard analytics and metrics"""
    METRIC_TYPES = [
        ('projects_total', 'Total Projects'),
        ('projects_active', 'Active Projects'),
        ('clients_total', 'Total Clients'),
        ('revenue_monthly', 'Monthly Revenue'),
        ('revenue_yearly', 'Yearly Revenue'),
        ('tasks_completed', 'Completed Tasks'),
        ('blog_views', 'Blog Views'),
        ('website_visitors', 'Website Visitors'),
    ]
    
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['metric_type', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value} ({self.date})"

class ActivityLog(models.Model):
    """Track user activities in admin dashboard"""
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=50, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.description}"
