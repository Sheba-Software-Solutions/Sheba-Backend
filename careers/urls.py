from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Job Postings (Admin)
    path('jobs/', views.JobPostingListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', views.JobPostingDetailView.as_view(), name='job-detail'),
    path('jobs/summary/', views.JobPostingSummaryListView.as_view(), name='job-summary'),
    
    # Job Applications (Admin)
    path('applications/', views.JobApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='application-detail'),
    
    # Statistics
    path('stats/', views.careers_stats, name='careers-stats'),
    
    # Public API endpoints for website (no authentication required)
    path('public/jobs/', views.PublicJobPostingListView.as_view(), name='public-job-list'),
    path('public/jobs/<slug:slug>/', views.PublicJobPostingDetailView.as_view(), name='public-job-detail'),
    path('public/apply/', views.PublicJobApplicationCreateView.as_view(), name='public-job-apply'),
]