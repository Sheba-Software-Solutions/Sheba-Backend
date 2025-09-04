from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # User management
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change-password'),
    
    # User sessions
    path('sessions/', views.UserSessionListView.as_view(), name='user-sessions'),
]
