from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Client(models.Model):
    """Client management model"""
    TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('startup', 'Startup'),
        ('small_business', 'Small Business'),
        ('enterprise', 'Enterprise'),
        ('government', 'Government'),
        ('ngo', 'NGO'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    client_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='individual')
    contact_person = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.company})" if self.company else self.name
    
    @property
    def total_projects(self):
        return self.projects.count()
    
    @property
    def active_projects(self):
        return self.projects.filter(status__in=['planning', 'in_progress', 'testing']).count()

class ClientContact(models.Model):
    """Additional contact persons for clients"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.client.name}"
