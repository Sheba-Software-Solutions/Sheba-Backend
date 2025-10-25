from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import JobPosting, JobApplication
from .serializers import (
    JobPostingSerializer, JobPostingSummarySerializer, PublicJobPostingSerializer,
    JobApplicationSerializer, JobApplicationSummarySerializer
)

class JobPostingListCreateView(generics.ListCreateAPIView):
    """List all job postings or create a new posting"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'department', 'job_type', 'experience_level']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['created_at', 'published_at', 'views', 'applications_count']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        # Automatically set the posted_by to the current user
        serializer.save(posted_by=self.request.user)

class JobPostingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a job posting"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]

class JobPostingSummaryListView(generics.ListAPIView):
    """List job postings with summary data"""
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'department', 'job_type']
    search_fields = ['title', 'location']
    ordering = ['-created_at']

class JobApplicationListCreateView(generics.ListCreateAPIView):
    """List all job applications or create a new application"""
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'job', 'job__department']
    search_fields = ['first_name', 'last_name', 'email', 'job__title']
    ordering_fields = ['submitted_at', 'years_of_experience']
    ordering = ['-submitted_at']

class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a job application"""
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def careers_stats(request):
    """Get careers statistics"""
    total_jobs = JobPosting.objects.count()
    published_jobs = JobPosting.objects.filter(status='published').count()
    total_applications = JobApplication.objects.count()
    pending_applications = JobApplication.objects.filter(status='submitted').count()
    
    # Department breakdown
    departments = JobPosting.objects.values('department').distinct()
    department_stats = {}
    for dept in departments:
        dept_name = dept['department']
        department_stats[dept_name] = {
            'jobs': JobPosting.objects.filter(department=dept_name).count(),
            'published_jobs': JobPosting.objects.filter(department=dept_name, status='published').count(),
            'applications': JobApplication.objects.filter(job__department=dept_name).count()
        }
    
    return Response({
        'total_jobs': total_jobs,
        'published_jobs': published_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'department_stats': department_stats
    })

# Public API Views for Website (No Authentication Required)

class PublicJobPostingListView(generics.ListAPIView):
    """Public list of published job postings for website"""
    queryset = JobPosting.objects.filter(status='published')
    serializer_class = PublicJobPostingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'job_type', 'experience_level', 'location']
    search_fields = ['title', 'description', 'location']
    ordering = ['-published_at', '-created_at']
    
    def get_queryset(self):
        # Increment view count for each job when listed
        queryset = super().get_queryset()
        # Note: In production, you might want to implement view counting differently
        # to avoid incrementing on every API call
        return queryset

class PublicJobPostingDetailView(generics.RetrieveAPIView):
    """Public job posting detail view"""
    queryset = JobPosting.objects.filter(status='published')
    serializer_class = PublicJobPostingSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PublicJobApplicationCreateView(generics.CreateAPIView):
    """Public job application submission"""
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        application = serializer.save()
        # Increment applications count for the job
        job = application.job
        job.applications_count += 1
        job.save(update_fields=['applications_count'])