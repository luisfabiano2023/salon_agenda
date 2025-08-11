from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from . import views_reports

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'professionals', views.ProfessionalViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'service-types', views.ServiceTypeViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'receptionists', views.ReceptionistViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    
    # Report endpoints
    path('reports/completed-services/', views_reports.completed_services_report, name='completed_services_report'),
    path('reports/performance-metrics/', views_reports.performance_metrics, name='performance_metrics'),
    path('reports/top-services/', views_reports.top_services, name='top_services'),
    path('reports/professional-performance/', views_reports.professional_performance, name='professional_performance'),
    path('reports/quick-stats/', views_reports.quick_stats, name='quick_stats'),
]

