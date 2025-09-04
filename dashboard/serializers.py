from rest_framework import serializers
from .models import DashboardMetric, ActivityLog
from authentication.serializers import UserProfileSerializer

class DashboardMetricSerializer(serializers.ModelSerializer):
    """Serializer for DashboardMetric model"""
    metric_type_display = serializers.CharField(source='get_metric_type_display', read_only=True)
    
    class Meta:
        model = DashboardMetric
        fields = ['id', 'metric_type', 'metric_type_display', 'value', 'date', 'created_at']
        read_only_fields = ['id', 'created_at']

class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model"""
    user = UserProfileSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'user_id', 'action', 'action_display', 'model_name',
                 'object_id', 'description', 'ip_address', 'user_agent', 'created_at']
        read_only_fields = ['id', 'created_at']
