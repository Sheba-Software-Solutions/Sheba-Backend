from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Website Content
    path('website/', views.WebsiteContentListCreateView.as_view(), name='website-content-list-create'),
    path('website/<int:pk>/', views.WebsiteContentDetailView.as_view(), name='website-content-detail'),
    
    # Blog Posts
    path('blog/', views.BlogPostListCreateView.as_view(), name='blog-list-create'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('blog/summary/', views.BlogPostSummaryListView.as_view(), name='blog-summary'),
    
    # Portfolio Projects
    path('portfolio/', views.PortfolioProjectListCreateView.as_view(), name='portfolio-list-create'),
    path('portfolio/<int:pk>/', views.PortfolioProjectDetailView.as_view(), name='portfolio-detail'),
    
    # Services
    path('services/', views.ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    
    # Team Members
    path('team/', views.TeamMemberListCreateView.as_view(), name='team-list-create'),
    path('team/<int:pk>/', views.TeamMemberDetailView.as_view(), name='team-detail'),
    
    # Statistics
    path('stats/', views.content_stats, name='content-stats'),
]
