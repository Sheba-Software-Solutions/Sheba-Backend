from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from datetime import timedelta
from .models import DashboardMetric, ActivityLog
from .serializers import DashboardMetricSerializer, ActivityLogSerializer
from projects.models import Project
from clients.models import Client
from content.models import BlogPost
from communication.models import ContactSubmission

class DashboardMetricListCreateView(generics.ListCreateAPIView):
    """List all dashboard metrics or create a new metric"""
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['metric_type', 'date']
    ordering = ['-date', '-created_at']

class DashboardMetricDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a dashboard metric"""
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActivityLogListCreateView(generics.ListCreateAPIView):
    """List all activity logs or create a new log"""
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['action', 'model_name', 'user']
    search_fields = ['description', 'model_name']
    ordering = ['-created_at']

class ActivityLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an activity log"""
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@cache_page(60 * 2)  # Cache for 2 minutes
def dashboard_overview(request):
    """Get dashboard overview statistics"""
    # Project statistics
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='in_progress').count()
    completed_projects = Project.objects.filter(status='completed').count()
    
    # Client statistics
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(is_active=True).count()
    
    # Content statistics
    total_blog_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(status='published').count()
    
    # Communication statistics
    pending_contacts = ContactSubmission.objects.filter(status='new').count()
    
    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_activities = ActivityLog.objects.filter(created_at__gte=week_ago).count()
    
    return Response({
        'projects': {
            'total': total_projects,
            'active': active_projects,
            'completed': completed_projects,
            'completion_rate': round((completed_projects / total_projects * 100) if total_projects > 0 else 0, 2)
        },
        'clients': {
            'total': total_clients,
            'active': active_clients
        },
        'content': {
            'blog_posts': total_blog_posts,
            'published_posts': published_posts
        },
        'communication': {
            'pending_contacts': pending_contacts
        },
        'activity': {
            'recent_activities': recent_activities
        }
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_metrics_chart(request):
    """Get metrics data for charts"""
    metric_type = request.GET.get('type', 'projects')
    days = int(request.GET.get('days', 30))
    
    start_date = timezone.now().date() - timedelta(days=days)
    metrics = DashboardMetric.objects.filter(
        metric_type=metric_type,
        date__gte=start_date
    ).order_by('date')
    
    return Response(DashboardMetricSerializer(metrics, many=True).data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recent_activities(request):
    """Get recent user activities"""
    limit = int(request.GET.get('limit', 10))
    activities = ActivityLog.objects.all()[:limit]
    return Response(ActivityLogSerializer(activities, many=True).data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_combined(request):
    """Get all dashboard data in a single request to reduce API calls"""
    # Project statistics
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='in_progress').count()
    completed_projects = Project.objects.filter(status='completed').count()
    
    # Client statistics
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(is_active=True).count()
    
    # Content statistics
    total_blog_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(status='published').count()
    
    # Communication statistics
    pending_contacts = ContactSubmission.objects.filter(status='new').count()
    
    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_activities_count = ActivityLog.objects.filter(created_at__gte=week_ago).count()
    
    # Recent activities (limited)
    limit = int(request.GET.get('limit', 10))
    recent_activities = ActivityLog.objects.all()[:limit]
    
    # Basic metrics for chart (last 30 days)
    start_date = timezone.now().date() - timedelta(days=30)
    metrics = DashboardMetric.objects.filter(
        metric_type='revenue_monthly',
        date__gte=start_date
    ).order_by('date')
    
    return Response({
        'overview': {
            'projects': {
                'total': total_projects,
                'active': active_projects,
                'completed': completed_projects,
                'completion_rate': round((completed_projects / total_projects * 100) if total_projects > 0 else 0, 2)
            },
            'clients': {
                'total': total_clients,
                'active': active_clients
            },
            'content': {
                'blog_posts': total_blog_posts,
                'published_posts': published_posts
            },
            'communication': {
                'pending_contacts': pending_contacts
            },
            'activity': {
                'recent_activities': recent_activities_count
            }
        },
        'recent_activities': ActivityLogSerializer(recent_activities, many=True).data,
        'metrics_chart': DashboardMetricSerializer(metrics, many=True).data
    })
