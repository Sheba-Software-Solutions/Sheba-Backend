from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    # Clients
    path('', views.ClientListCreateView.as_view(), name='client-list-create'),
    path('<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('summary/', views.ClientSummaryListView.as_view(), name='client-summary'),
    path('stats/', views.client_stats, name='client-stats'),
    
    # Client Contacts
    path('contacts/', views.ClientContactListCreateView.as_view(), name='contact-list-create'),
    path('<int:client_id>/contacts/', views.ClientContactListCreateView.as_view(), name='client-contact-list-create'),
    path('contacts/<int:pk>/', views.ClientContactDetailView.as_view(), name='contact-detail'),
]
