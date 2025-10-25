from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Metrics
    path('metrics/', views.DashboardMetricListCreateView.as_view(), name='metric-list-create'),
    path('metrics/<int:pk>/', views.DashboardMetricDetailView.as_view(), name='metric-detail'),
    path('metrics/chart/', views.dashboard_metrics_chart, name='metrics-chart'),
    
    # Activity Logs
    path('activities/', views.ActivityLogListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', views.ActivityLogDetailView.as_view(), name='activity-detail'),
    path('activities/recent/', views.recent_activities, name='recent-activities'),
    
    # Dashboard Overview
    path('overview/', views.dashboard_overview, name='dashboard-overview'),
    path('combined/', views.dashboard_combined, name='dashboard-combined'),
]
