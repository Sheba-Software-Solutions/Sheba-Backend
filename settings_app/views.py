from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import CompanySettings, SystemSettings, UserPermission, SystemLog
from .serializers import (
    CompanySettingsSerializer, SystemSettingsSerializer, 
    UserPermissionSerializer, SystemLogSerializer
)

class CompanySettingsView(generics.RetrieveUpdateAPIView):
    """Get or update company settings"""
    queryset = CompanySettings.objects.all()
    serializer_class = CompanySettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        # Get or create the single company settings instance
        obj, created = CompanySettings.objects.get_or_create(pk=1)
        return obj

class SystemSettingsView(generics.RetrieveUpdateAPIView):
    """Get or update system settings"""
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_object(self):
        # Get or create the single system settings instance
        obj, created = SystemSettings.objects.get_or_create(pk=1)
        return obj

class UserPermissionListCreateView(generics.ListCreateAPIView):
    """List all user permissions or create a new permission"""
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'permission', 'granted']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']

class UserPermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a user permission"""
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class SystemLogListView(generics.ListAPIView):
    """List all system logs"""
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['level', 'module', 'user']
    search_fields = ['message', 'module']
    ordering = ['-created_at']

class SystemLogDetailView(generics.RetrieveAPIView):
    """Retrieve a system log"""
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_permissions(request, user_id):
    """Get permissions for a specific user"""
    permissions_list = UserPermission.objects.filter(user_id=user_id, granted=True)
    return Response(UserPermissionSerializer(permissions_list, many=True).data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def backup_database(request):
    """Trigger database backup"""
    # This would implement actual backup logic
    return Response({'message': 'Database backup initiated'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def restore_database(request):
    """Trigger database restore"""
    # This would implement actual restore logic
    return Response({'message': 'Database restore initiated'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
def system_health(request):
    """Get system health status"""
    # This would implement actual health checks
    return Response({
        'status': 'healthy',
        'database': 'connected',
        'storage': 'available',
        'memory_usage': '45%',
        'cpu_usage': '23%'
    })
