from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import WebsiteContent, BlogPost, PortfolioProject, Service, TeamMember
from .serializers import (
    WebsiteContentSerializer, BlogPostSerializer, BlogPostSummarySerializer,
    PortfolioProjectSerializer, ServiceSerializer, TeamMemberSerializer
)

class WebsiteContentListCreateView(generics.ListCreateAPIView):
    """List all website content or create new content"""
    queryset = WebsiteContent.objects.all()
    serializer_class = WebsiteContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['section', 'is_active']
    search_fields = ['title', 'content']
    ordering = ['section', '-updated_at']

class WebsiteContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete website content"""
    queryset = WebsiteContent.objects.all()
    serializer_class = WebsiteContentSerializer
    permission_classes = [permissions.IsAuthenticated]

class BlogPostListCreateView(generics.ListCreateAPIView):
    """List all blog posts or create a new post"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'published_at', 'views']
    ordering = ['-created_at']

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a blog post"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

class BlogPostSummaryListView(generics.ListAPIView):
    """List blog posts with summary data"""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['title']
    ordering = ['-created_at']

class PortfolioProjectListCreateView(generics.ListCreateAPIView):
    """List all portfolio projects or create a new project"""
    queryset = PortfolioProject.objects.all()
    serializer_class = PortfolioProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']

class PortfolioProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a portfolio project"""
    queryset = PortfolioProject.objects.all()
    serializer_class = PortfolioProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class ServiceListCreateView(generics.ListCreateAPIView):
    """List all services or create a new service"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a service"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class TeamMemberListCreateView(generics.ListCreateAPIView):
    """List all team members or create a new member"""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'role', 'bio']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']

class TeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a team member"""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def content_stats(request):
    """Get content statistics"""
    blog_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(status='published').count()
    portfolio_projects = PortfolioProject.objects.count()
    active_services = Service.objects.filter(status='active').count()
    team_members = TeamMember.objects.filter(status='active').count()
    
    return Response({
        'blog_posts': blog_posts,
        'published_posts': published_posts,
        'portfolio_projects': portfolio_projects,
        'active_services': active_services,
        'team_members': team_members
    })
