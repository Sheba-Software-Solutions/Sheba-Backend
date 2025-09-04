from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    # Contact Submissions
    path('contacts/', views.ContactSubmissionListCreateView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', views.ContactSubmissionDetailView.as_view(), name='contact-detail'),
    
    # Email Templates
    path('email-templates/', views.EmailTemplateListCreateView.as_view(), name='email-template-list-create'),
    path('email-templates/<int:pk>/', views.EmailTemplateDetailView.as_view(), name='email-template-detail'),
    
    # Newsletters
    path('newsletters/', views.NewsletterListCreateView.as_view(), name='newsletter-list-create'),
    path('newsletters/<int:pk>/', views.NewsletterDetailView.as_view(), name='newsletter-detail'),
    
    # Newsletter Subscribers
    path('subscribers/', views.NewsletterSubscriberListCreateView.as_view(), name='subscriber-list-create'),
    path('subscribers/<int:pk>/', views.NewsletterSubscriberDetailView.as_view(), name='subscriber-detail'),
    
    # Notifications
    path('notifications/', views.NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='notification-mark-read'),
    
    # Statistics
    path('stats/', views.communication_stats, name='communication-stats'),
]
