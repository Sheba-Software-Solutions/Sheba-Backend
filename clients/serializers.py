from rest_framework import serializers
from .models import Client, ClientContact

class ClientContactSerializer(serializers.ModelSerializer):
    """Serializer for ClientContact model"""
    class Meta:
        model = ClientContact
        fields = ['id', 'name', 'email', 'phone', 'position', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']

class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model"""
    contacts = ClientContactSerializer(many=True, read_only=True)
    total_projects = serializers.ReadOnlyField()
    active_projects = serializers.ReadOnlyField()
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'company', 'website', 'address',
                 'client_type', 'contact_person', 'notes', 'is_active', 'contacts',
                 'total_projects', 'active_projects', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClientSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for client summaries"""
    total_projects = serializers.ReadOnlyField()
    active_projects = serializers.ReadOnlyField()
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'company', 'email', 'client_type', 'is_active',
                 'total_projects', 'active_projects']
