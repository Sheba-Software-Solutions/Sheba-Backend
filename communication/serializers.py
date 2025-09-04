from rest_framework import serializers
from .models import ContactSubmission, EmailTemplate, Newsletter, NewsletterSubscriber, Notification
from authentication.serializers import UserProfileSerializer

class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for ContactSubmission model"""
    assigned_to = UserProfileSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'status',
                 'assigned_to', 'assigned_to_id', 'response', 'ip_address', 'user_agent',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'ip_address', 'user_agent', 'created_at', 'updated_at']

class EmailTemplateSerializer(serializers.ModelSerializer):
    """Serializer for EmailTemplate model"""
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'template_type', 'subject', 'content', 'is_active',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for Newsletter model"""
    created_by = UserProfileSerializer(read_only=True)
    created_by_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Newsletter
        fields = ['id', 'title', 'content', 'status', 'scheduled_at', 'sent_at',
                 'recipients_count', 'opened_count', 'clicked_count', 'created_by',
                 'created_by_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'sent_at', 'recipients_count', 'opened_count', 
                           'clicked_count', 'created_at', 'updated_at']

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    """Serializer for NewsletterSubscriber model"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['id', 'email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
        read_only_fields = ['id', 'subscribed_at', 'unsubscribed_at']

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    recipient = UserProfileSerializer(read_only=True)
    recipient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'recipient',
                 'recipient_id', 'is_read', 'action_url', 'created_at']
        read_only_fields = ['id', 'created_at']
