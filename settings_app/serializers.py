from rest_framework import serializers
from .models import CompanySettings, SystemSettings, UserPermission, SystemLog
from authentication.serializers import UserProfileSerializer

class CompanySettingsSerializer(serializers.ModelSerializer):
    """Serializer for CompanySettings model"""
    class Meta:
        model = CompanySettings
        fields = ['id', 'name', 'tagline', 'description', 'email', 'phone', 'address',
                 'website', 'logo', 'favicon', 'facebook_url', 'twitter_url', 'linkedin_url',
                 'instagram_url', 'github_url', 'tax_id', 'registration_number', 'updated_at']
        read_only_fields = ['id', 'updated_at']

class SystemSettingsSerializer(serializers.ModelSerializer):
    """Serializer for SystemSettings model"""
    class Meta:
        model = SystemSettings
        fields = ['id', 'smtp_host', 'smtp_port', 'smtp_username', 'smtp_password',
                 'smtp_use_tls', 'auto_backup_enabled', 'backup_frequency', 'session_timeout',
                 'max_login_attempts', 'password_expiry_days', 'api_rate_limit', 'updated_at']
        read_only_fields = ['id', 'updated_at']
        extra_kwargs = {
            'smtp_password': {'write_only': True}
        }

class UserPermissionSerializer(serializers.ModelSerializer):
    """Serializer for UserPermission model"""
    user = UserProfileSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    granted_by = UserProfileSerializer(read_only=True)
    granted_by_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    permission_display = serializers.CharField(source='get_permission_display', read_only=True)
    
    class Meta:
        model = UserPermission
        fields = ['id', 'user', 'user_id', 'permission', 'permission_display', 'granted',
                 'granted_by', 'granted_by_id', 'created_at']
        read_only_fields = ['id', 'created_at']

class SystemLogSerializer(serializers.ModelSerializer):
    """Serializer for SystemLog model"""
    user = UserProfileSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = SystemLog
        fields = ['id', 'level', 'level_display', 'message', 'module', 'user', 'user_id',
                 'ip_address', 'extra_data', 'created_at']
        read_only_fields = ['id', 'created_at']
