from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ContactSubmission, EmailTemplate, Newsletter, NewsletterSubscriber, Notification
from .serializers import (
    ContactSubmissionSerializer, EmailTemplateSerializer, NewsletterSerializer,
    NewsletterSubscriberSerializer, NotificationSerializer
)

class ContactSubmissionListCreateView(generics.ListCreateAPIView):
    """List all contact submissions or create a new submission"""
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'assigned_to']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

class ContactSubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a contact submission"""
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmailTemplateListCreateView(generics.ListCreateAPIView):
    """List all email templates or create a new template"""
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['template_type', 'is_active']
    search_fields = ['name', 'subject', 'content']
    ordering = ['-created_at']

class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an email template"""
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

class NewsletterListCreateView(generics.ListCreateAPIView):
    """List all newsletters or create a new newsletter"""
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'created_by']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'scheduled_at', 'sent_at']
    ordering = ['-created_at']

class NewsletterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a newsletter"""
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]

class NewsletterSubscriberListCreateView(generics.ListCreateAPIView):
    """List all newsletter subscribers or create a new subscriber"""
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['email', 'name']
    ordering = ['-subscribed_at']

class NewsletterSubscriberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a newsletter subscriber"""
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationListCreateView(generics.ListCreateAPIView):
    """List all notifications or create a new notification"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['notification_type', 'recipient', 'is_read']
    search_fields = ['title', 'message']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see their own notifications unless they're admin
        if self.request.user.is_staff or self.request.user.role == 'admin':
            return Notification.objects.all()
        return Notification.objects.filter(recipient=self.request.user)

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a notification"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only access their own notifications unless they're admin
        if self.request.user.is_staff or self.request.user.role == 'admin':
            return Notification.objects.all()
        return Notification.objects.filter(recipient=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """Mark a notification as read"""
    try:
        if request.user.is_staff or request.user.role == 'admin':
            notification = Notification.objects.get(pk=pk)
        else:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def communication_stats(request):
    """Get communication statistics"""
    contact_submissions = ContactSubmission.objects.count()
    pending_submissions = ContactSubmission.objects.filter(status='new').count()
    newsletter_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()
    sent_newsletters = Newsletter.objects.filter(status='sent').count()
    
    return Response({
        'contact_submissions': contact_submissions,
        'pending_submissions': pending_submissions,
        'newsletter_subscribers': newsletter_subscribers,
        'sent_newsletters': sent_newsletters
    })
