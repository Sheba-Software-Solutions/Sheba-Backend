from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Project, ProjectTask
from .serializers import ProjectSerializer, ProjectTaskSerializer, ProjectSummarySerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    """List all projects or create a new project"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'client']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'priority']
    ordering = ['-created_at']

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a project"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectSummaryListView(generics.ListAPIView):
    """List projects with summary data"""
    queryset = Project.objects.all()
    serializer_class = ProjectSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['name']
    ordering = ['-created_at']

class ProjectTaskListCreateView(generics.ListCreateAPIView):
    """List tasks for a project or create a new task"""
    serializer_class = ProjectTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if project_id:
            return ProjectTask.objects.filter(project_id=project_id)
        return ProjectTask.objects.all()
    
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        if project_id:
            serializer.save(project_id=project_id)
        else:
            serializer.save()

class ProjectTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a project task"""
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def project_stats(request):
    """Get project statistics"""
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='in_progress').count()
    completed_projects = Project.objects.filter(status='completed').count()
    on_hold_projects = Project.objects.filter(status='on_hold').count()
    
    return Response({
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'on_hold_projects': on_hold_projects,
        'completion_rate': round((completed_projects / total_projects * 100) if total_projects > 0 else 0, 2)
    })
