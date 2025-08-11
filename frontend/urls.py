from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_page, name='login'),
    path('clients/', views.clients, name='clients'),
    path('professionals/', views.professionals, name='professionals'),
    path('services/', views.services, name='services'),
    path('appointments/', views.appointments, name='appointments'),
    path('reports/', views.reports, name='reports'),
]

