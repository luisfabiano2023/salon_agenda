from django.db import models
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, ServiceType, Professional, Client


class ServiceReportManager:
    """Manager class for generating service completion reports"""
    
    @staticmethod
    def get_completed_services_report(start_date=None, end_date=None, professional_id=None, service_type_id=None):
        """
        Generate a comprehensive report of completed services within a date range.
        
        Args:
            start_date (date): Start date for the report (inclusive)
            end_date (date): End date for the report (inclusive)
            professional_id (str): Filter by specific professional
            service_type_id (str): Filter by specific service type
            
        Returns:
            dict: Report data with statistics and details
        """
        # Base queryset for completed appointments
        queryset = Appointment.objects.filter(status='completed')
        
        # Apply date filters
        if start_date:
            queryset = queryset.filter(scheduled_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(scheduled_date__lte=end_date)
        
        # Apply professional filter
        if professional_id:
            queryset = queryset.filter(professional_id=professional_id)
            
        # Apply service type filter
        if service_type_id:
            queryset = queryset.filter(service_type_id=service_type_id)
        
        # Optimize query with select_related to avoid N+1 queries
        queryset = queryset.select_related('client', 'professional', 'service_type')
        
        # Calculate summary statistics
        summary_stats = queryset.aggregate(
            total_services=Count('id'),
            total_revenue=Sum('price'),
            avg_price=models.Avg('price'),
            total_duration=Sum('duration_minutes')
        )
        
        # Services by type
        services_by_type = (
            queryset.values('service_type__name', 'service_type__id')
            .annotate(
                count=Count('id'),
                revenue=Sum('price'),
                avg_duration=models.Avg('duration_minutes')
            )
            .order_by('-count')
        )
        
        # Services by professional
        services_by_professional = (
            queryset.values('professional__name', 'professional__id')
            .annotate(
                count=Count('id'),
                revenue=Sum('price'),
                avg_duration=models.Avg('duration_minutes')
            )
            .order_by('-count')
        )
        
        # Daily breakdown
        daily_breakdown = (
            queryset.values('scheduled_date')
            .annotate(
                count=Count('id'),
                revenue=Sum('price')
            )
            .order_by('scheduled_date')
        )
        
        return {
            'summary': {
                'total_services': summary_stats['total_services'] or 0,
                'total_revenue': float(summary_stats['total_revenue'] or 0),
                'average_price': float(summary_stats['avg_price'] or 0),
                'total_duration_hours': round((summary_stats['total_duration'] or 0) / 60, 2),
                'period': {
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None
                }
            },
            'services_by_type': list(services_by_type),
            'services_by_professional': list(services_by_professional),
            'daily_breakdown': list(daily_breakdown)
        }
    
    @staticmethod
    def get_performance_metrics(start_date=None, end_date=None):
        """
        Get performance metrics for the salon.
        
        Args:
            start_date (date): Start date for metrics
            end_date (date): End date for metrics
            
        Returns:
            dict: Performance metrics
        """
        # Base queryset
        queryset = Appointment.objects.all()
        
        if start_date:
            queryset = queryset.filter(scheduled_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(scheduled_date__lte=end_date)
        
        # Calculate metrics by status
        status_breakdown = (
            queryset.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        
        # Calculate completion rate
        total_appointments = queryset.count()
        completed_appointments = queryset.filter(status='completed').count()
        completion_rate = (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0
        
        # Calculate cancellation rate
        cancelled_appointments = queryset.filter(status='cancelled').count()
        cancellation_rate = (cancelled_appointments / total_appointments * 100) if total_appointments > 0 else 0
        
        # Calculate no-show rate
        no_show_appointments = queryset.filter(status='no_show').count()
        no_show_rate = (no_show_appointments / total_appointments * 100) if total_appointments > 0 else 0
        
        return {
            'total_appointments': total_appointments,
            'completed_appointments': completed_appointments,
            'completion_rate': round(completion_rate, 2),
            'cancellation_rate': round(cancellation_rate, 2),
            'no_show_rate': round(no_show_rate, 2),
            'status_breakdown': list(status_breakdown)
        }
    
    @staticmethod
    def get_top_services(start_date=None, end_date=None, limit=10):
        """
        Get the most popular services by completion count.
        
        Args:
            start_date (date): Start date for analysis
            end_date (date): End date for analysis
            limit (int): Number of top services to return
            
        Returns:
            list: Top services with statistics
        """
        queryset = Appointment.objects.filter(status='completed')
        
        if start_date:
            queryset = queryset.filter(scheduled_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(scheduled_date__lte=end_date)
        
        top_services = (
            queryset.values('service_type__name', 'service_type__base_price')
            .annotate(
                completion_count=Count('id'),
                total_revenue=Sum('price'),
                avg_price=models.Avg('price')
            )
            .order_by('-completion_count')[:limit]
        )
        
        return list(top_services)
    
    @staticmethod
    def get_professional_performance(start_date=None, end_date=None):
        """
        Get performance metrics for each professional.
        
        Args:
            start_date (date): Start date for analysis
            end_date (date): End date for analysis
            
        Returns:
            list: Professional performance data
        """
        queryset = Appointment.objects.filter(status='completed')
        
        if start_date:
            queryset = queryset.filter(scheduled_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(scheduled_date__lte=end_date)
        
        professional_stats = (
            queryset.values('professional__name', 'professional__id')
            .annotate(
                services_completed=Count('id'),
                total_revenue=Sum('price'),
                avg_service_price=models.Avg('price'),
                total_hours_worked=Sum('duration_minutes') / 60.0
            )
            .order_by('-services_completed')
        )
        
        return list(professional_stats)


class ReportOptimizer:
    """Class for optimizing report queries for large datasets"""
    
    @staticmethod
    def create_database_indexes():
        """
        Suggest database indexes for optimal report performance.
        These should be added as Django migrations.
        """
        suggested_indexes = [
            # For appointment queries
            "CREATE INDEX IF NOT EXISTS idx_appointment_status_date ON api_appointment(status, scheduled_date);",
            "CREATE INDEX IF NOT EXISTS idx_appointment_professional_date ON api_appointment(professional_id, scheduled_date);",
            "CREATE INDEX IF NOT EXISTS idx_appointment_service_date ON api_appointment(service_type_id, scheduled_date);",
            "CREATE INDEX IF NOT EXISTS idx_appointment_date_status ON api_appointment(scheduled_date, status);",
            
            # For performance optimization
            "CREATE INDEX IF NOT EXISTS idx_appointment_completed_date ON api_appointment(scheduled_date) WHERE status = 'completed';",
        ]
        
        return suggested_indexes
    
    @staticmethod
    def get_optimized_completed_services_count(start_date=None, end_date=None):
        """
        Optimized query for getting just the count of completed services.
        This is much faster for large datasets when you only need the count.
        """
        queryset = Appointment.objects.filter(status='completed')
        
        if start_date:
            queryset = queryset.filter(scheduled_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(scheduled_date__lte=end_date)
        
        # Use only() to fetch only the necessary fields for counting
        return queryset.only('id').count()

