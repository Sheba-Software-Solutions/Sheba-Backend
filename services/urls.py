from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListCreateView.as_view(), name='service-list'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('active/', views.ActiveServiceListView.as_view(), name='active-services'),
]
