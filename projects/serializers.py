from rest_framework import serializers
from .models import Project, ProjectTask
from clients.serializers import ClientSerializer
from authentication.serializers import UserProfileSerializer

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    client = ClientSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True)
    assigned_to = UserProfileSerializer(many=True, read_only=True)
    assigned_to_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    tasks_count = serializers.SerializerMethodField()
    completed_tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'client', 'client_id', 'assigned_to', 
                 'assigned_to_ids', 'status', 'priority', 'start_date', 'end_date', 
                 'budget', 'progress', 'technologies', 'repository_url', 'live_url',
                 'tasks_count', 'completed_tasks_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_tasks_count(self, obj):
        return obj.tasks.count()
    
    def get_completed_tasks_count(self, obj):
        return obj.tasks.filter(status='completed').count()
    
    def create(self, validated_data):
        assigned_to_ids = validated_data.pop('assigned_to_ids', [])
        project = Project.objects.create(**validated_data)
        if assigned_to_ids:
            project.assigned_to.set(assigned_to_ids)
        return project
    
    def update(self, instance, validated_data):
        assigned_to_ids = validated_data.pop('assigned_to_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if assigned_to_ids is not None:
            instance.assigned_to.set(assigned_to_ids)
        return instance

class ProjectTaskSerializer(serializers.ModelSerializer):
    """Serializer for ProjectTask model"""
    project = ProjectSerializer(read_only=True)
    project_id = serializers.IntegerField(write_only=True)
    assigned_to = UserProfileSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProjectTask
        fields = ['id', 'project', 'project_id', 'title', 'description', 'assigned_to',
                 'assigned_to_id', 'status', 'due_date', 'estimated_hours', 'actual_hours',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProjectSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for project summaries"""
    client_name = serializers.CharField(source='client.name', read_only=True)
    tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'client_name', 'status', 'priority', 'progress',
                 'start_date', 'end_date', 'tasks_count']
    
    def get_tasks_count(self, obj):
        return obj.tasks.count()

class PublicProjectSerializer(serializers.ModelSerializer):
    """Serializer for public website project showcase"""
    client_name = serializers.CharField(source='client.name', read_only=True)
    client_company = serializers.CharField(source='client.company', read_only=True)
    tasks_count = serializers.SerializerMethodField()
    completed_tasks_count = serializers.SerializerMethodField()
    team_size = serializers.SerializerMethodField()
    duration_days = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'client_name', 'client_company',
            'status', 'priority', 'progress', 'start_date', 'end_date',
            'technologies', 'repository_url', 'live_url', 'tasks_count',
            'completed_tasks_count', 'team_size', 'duration_days', 'created_at'
        ]
    
    def get_tasks_count(self, obj):
        return obj.tasks.count()
    
    def get_completed_tasks_count(self, obj):
        return obj.tasks.filter(status='completed').count()
    
    def get_team_size(self, obj):
        return obj.assigned_to.count()
    
    def get_duration_days(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None
