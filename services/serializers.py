from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for the Service model"""
    features_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'icon', 'order', 'is_active', 'features', 'features_list',
            'price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_features_list(self, obj):
        ""
        Return features as a list instead of newline-separated string
        """
        return obj.get_features_list()
