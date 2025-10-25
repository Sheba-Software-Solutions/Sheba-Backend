from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPosting(models.Model):
    """Job posting model for career opportunities"""
    
    DEPARTMENT_CHOICES = [
        ('engineering', 'Engineering'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('operations', 'Operations'),
    ]
    
    TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level (0-1 years)'),
        ('junior', 'Junior (1-3 years)'),
        ('mid', 'Mid Level (3-5 years)'),
        ('senior', 'Senior (5+ years)'),
        ('lead', 'Lead/Principal (8+ years)'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    
    description = models.TextField()
    requirements = models.JSONField(default=list, help_text="List of job requirements")
    responsibilities = models.JSONField(default=list, help_text="List of job responsibilities")
    benefits = models.JSONField(default=list, help_text="List of benefits")
    
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='ETB')
    salary_display = models.CharField(max_length=50, default='Competitive', help_text="Display text for salary")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_postings')
    
    application_deadline = models.DateField(null=True, blank=True)
    application_email = models.EmailField(blank=True)
    application_url = models.URLField(blank=True)
    
    views = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'department']),
            models.Index(fields=['published_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.department}"
    
    @property
    def is_published(self):
        return self.status == 'published'
    
    @property
    def salary_range(self):
        if self.salary_min and self.salary_max:
            return f"{self.salary_min:,.0f} - {self.salary_max:,.0f} {self.salary_currency}"
        return self.salary_display

class JobApplication(models.Model):
    """Job application model"""
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    
    # Applicant Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Application Details
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Experience
    years_of_experience = models.PositiveIntegerField(default=0)
    current_position = models.CharField(max_length=200, blank=True)
    current_company = models.CharField(max_length=200, blank=True)
    
    # Status and Notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['job', 'email']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"