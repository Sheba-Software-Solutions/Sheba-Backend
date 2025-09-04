from rest_framework import serializers
from .models import WebsiteContent, BlogPost, PortfolioProject, Service, TeamMember
from authentication.serializers import UserProfileSerializer

class WebsiteContentSerializer(serializers.ModelSerializer):
    """Serializer for WebsiteContent model"""
    class Meta:
        model = WebsiteContent
        fields = ['id', 'section', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'author', 'author_id',
                 'category', 'status', 'featured_image', 'views', 'published_at',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'views', 'created_at', 'updated_at']

class BlogPostSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for blog post summaries"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'excerpt', 'author_name', 'category', 
                 'status', 'views', 'published_at', 'created_at']

class PortfolioProjectSerializer(serializers.ModelSerializer):
    """Serializer for PortfolioProject model"""
    class Meta:
        model = PortfolioProject
        fields = ['id', 'title', 'description', 'category', 'image', 'technologies',
                 'project_url', 'github_url', 'status', 'order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model"""
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'features', 'price', 'icon',
                 'status', 'order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for TeamMember model"""
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role', 'bio', 'email', 'phone', 'image',
                 'linkedin_url', 'github_url', 'status', 'order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
