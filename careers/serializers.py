from rest_framework import serializers
from .models import JobPosting, JobApplication
from authentication.serializers import UserProfileSerializer

class JobPostingSerializer(serializers.ModelSerializer):
    """Serializer for JobPosting model"""
    posted_by = UserProfileSerializer(read_only=True)
    posted_by_id = serializers.IntegerField(write_only=True, required=False)
    salary_range = serializers.ReadOnlyField()
    is_published = serializers.ReadOnlyField()
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'slug', 'department', 'location', 'job_type', 
            'experience_level', 'description', 'requirements', 'responsibilities', 
            'benefits', 'salary_min', 'salary_max', 'salary_currency', 
            'salary_display', 'salary_range', 'status', 'posted_by', 'posted_by_id',
            'application_deadline', 'application_email', 'application_url',
            'views', 'applications_count', 'is_published',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'views', 'applications_count', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set posted_by to current user if not provided
        if 'posted_by_id' not in validated_data:
            validated_data['posted_by'] = self.context['request'].user
        else:
            validated_data['posted_by_id'] = validated_data.pop('posted_by_id')
        
        # Set published_at when status is published
        if validated_data.get('status') == 'published' and not validated_data.get('published_at'):
            from django.utils import timezone
            validated_data['published_at'] = timezone.now()
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Handle posted_by_id if provided
        if 'posted_by_id' in validated_data:
            validated_data['posted_by_id'] = validated_data.pop('posted_by_id')
        
        # Set published_at when status changes to published
        if (validated_data.get('status') == 'published' and 
            instance.status != 'published' and 
            not instance.published_at):
            from django.utils import timezone
            validated_data['published_at'] = timezone.now()
        
        return super().update(instance, validated_data)

class JobPostingSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for job posting summaries"""
    posted_by_name = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    salary_range = serializers.ReadOnlyField()
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'slug', 'department', 'location', 'job_type',
            'experience_level', 'salary_range', 'status', 'posted_by_name',
            'application_deadline', 'views', 'applications_count', 'published_at'
        ]

class PublicJobPostingSerializer(serializers.ModelSerializer):
    """Serializer for public job posting display"""
    salary_range = serializers.ReadOnlyField()
    
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'slug', 'department', 'location', 'job_type',
            'experience_level', 'description', 'requirements', 'responsibilities',
            'benefits', 'salary_range', 'application_deadline', 'application_email',
            'application_url', 'published_at'
        ]

class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for JobApplication model"""
    job = JobPostingSummarySerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_id', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'cover_letter', 'resume', 'portfolio_url',
            'linkedin_url', 'years_of_experience', 'current_position',
            'current_company', 'status', 'admin_notes', 'submitted_at', 'updated_at'
        ]
        read_only_fields = ['id', 'submitted_at', 'updated_at']

class JobApplicationSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for job application summaries"""
    job_title = serializers.CharField(source='job.title', read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job_title', 'full_name', 'email', 'phone',
            'years_of_experience', 'current_position', 'status', 'submitted_at'
        ]