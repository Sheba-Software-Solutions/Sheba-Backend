from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    # Projects
    path("", views.ProjectListCreateView.as_view(), name="project-list-create"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path("summary/", views.ProjectSummaryListView.as_view(), name="project-summary"),
    path("stats/", views.project_stats, name="project-stats"),
    path("statistics/", views.project_stats, name="project-statistics"),
    # Project Tasks
    path("tasks/", views.ProjectTaskListCreateView.as_view(), name="task-list-create"),
    path(
        "<int:project_id>/tasks/",
        views.ProjectTaskListCreateView.as_view(),
        name="project-task-list-create",
    ),
    path("tasks/<int:pk>/", views.ProjectTaskDetailView.as_view(), name="task-detail"),
]
