from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Client, ClientContact
from .serializers import ClientSerializer, ClientContactSerializer, ClientSummarySerializer

class ClientListCreateView(generics.ListCreateAPIView):
    """List all clients or create a new client"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client_type', 'is_active']
    search_fields = ['name', 'company', 'email']
    ordering_fields = ['created_at', 'name', 'company']
    ordering = ['-created_at']

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a client"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClientSummaryListView(generics.ListAPIView):
    """List clients with summary data"""
    queryset = Client.objects.all()
    serializer_class = ClientSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['client_type', 'is_active']
    search_fields = ['name', 'company']
    ordering = ['-created_at']

class ClientContactListCreateView(generics.ListCreateAPIView):
    """List contacts for a client or create a new contact"""
    serializer_class = ClientContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        if client_id:
            return ClientContact.objects.filter(client_id=client_id)
        return ClientContact.objects.all()
    
    def perform_create(self, serializer):
        client_id = self.kwargs.get('client_id')
        if client_id:
            serializer.save(client_id=client_id)
        else:
            serializer.save()

class ClientContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a client contact"""
    queryset = ClientContact.objects.all()
    serializer_class = ClientContactSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def client_stats(request):
    """Get client statistics"""
    total_clients = Client.objects.count()
    active_clients = Client.objects.filter(is_active=True).count()
    individual_clients = Client.objects.filter(client_type='individual').count()
    business_clients = Client.objects.filter(client_type='business').count()
    
    return Response({
        'total_clients': total_clients,
        'active_clients': active_clients,
        'individual_clients': individual_clients,
        'business_clients': business_clients
    })
