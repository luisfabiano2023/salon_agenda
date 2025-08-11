from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import datetime, timedelta
from .reports import ServiceReportManager, ReportOptimizer
from .models import Professional, ServiceType


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def completed_services_report(request):
    """
    API endpoint for getting completed services report.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD format)
    - end_date: End date (YYYY-MM-DD format)
    - professional_id: Filter by professional UUID
    - service_type_id: Filter by service type UUID
    """
    try:
        # Parse query parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        professional_id = request.GET.get('professional_id')
        service_type_id = request.GET.get('service_type_id')
        
        # Parse dates
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = parse_date(start_date_str)
            if not start_date:
                return Response(
                    {'error': 'Invalid start_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if end_date_str:
            end_date = parse_date(end_date_str)
            if not end_date:
                return Response(
                    {'error': 'Invalid end_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Validate date range
        if start_date and end_date and start_date > end_date:
            return Response(
                {'error': 'start_date cannot be after end_date.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate professional_id if provided
        if professional_id:
            try:
                Professional.objects.get(id=professional_id)
            except Professional.DoesNotExist:
                return Response(
                    {'error': 'Professional not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Validate service_type_id if provided
        if service_type_id:
            try:
                ServiceType.objects.get(id=service_type_id)
            except ServiceType.DoesNotExist:
                return Response(
                    {'error': 'Service type not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Generate report
        report_data = ServiceReportManager.get_completed_services_report(
            start_date=start_date,
            end_date=end_date,
            professional_id=professional_id,
            service_type_id=service_type_id
        )
        
        return Response(report_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'An error occurred while generating the report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performance_metrics(request):
    """
    API endpoint for getting salon performance metrics.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD format)
    - end_date: End date (YYYY-MM-DD format)
    """
    try:
        # Parse query parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        # Parse dates
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = parse_date(start_date_str)
            if not start_date:
                return Response(
                    {'error': 'Invalid start_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if end_date_str:
            end_date = parse_date(end_date_str)
            if not end_date:
                return Response(
                    {'error': 'Invalid end_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Generate performance metrics
        metrics_data = ServiceReportManager.get_performance_metrics(
            start_date=start_date,
            end_date=end_date
        )
        
        return Response(metrics_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'An error occurred while generating metrics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_services(request):
    """
    API endpoint for getting top services by completion count.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD format)
    - end_date: End date (YYYY-MM-DD format)
    - limit: Number of top services to return (default: 10)
    """
    try:
        # Parse query parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        limit_str = request.GET.get('limit', '10')
        
        # Parse limit
        try:
            limit = int(limit_str)
            if limit <= 0:
                limit = 10
        except ValueError:
            limit = 10
        
        # Parse dates
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = parse_date(start_date_str)
            if not start_date:
                return Response(
                    {'error': 'Invalid start_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if end_date_str:
            end_date = parse_date(end_date_str)
            if not end_date:
                return Response(
                    {'error': 'Invalid end_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get top services
        top_services_data = ServiceReportManager.get_top_services(
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        
        return Response({
            'top_services': top_services_data,
            'limit': limit,
            'period': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'An error occurred while getting top services: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def professional_performance(request):
    """
    API endpoint for getting professional performance metrics.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD format)
    - end_date: End date (YYYY-MM-DD format)
    """
    try:
        # Parse query parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        # Parse dates
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = parse_date(start_date_str)
            if not start_date:
                return Response(
                    {'error': 'Invalid start_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if end_date_str:
            end_date = parse_date(end_date_str)
            if not end_date:
                return Response(
                    {'error': 'Invalid end_date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get professional performance data
        performance_data = ServiceReportManager.get_professional_performance(
            start_date=start_date,
            end_date=end_date
        )
        
        return Response({
            'professional_performance': performance_data,
            'period': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'An error occurred while getting professional performance: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def quick_stats(request):
    """
    API endpoint for getting quick statistics for dashboard.
    Optimized for performance with large datasets.
    """
    try:
        # Get today's date
        today = timezone.now().date()
        
        # Get quick stats using optimized queries
        today_completed = ReportOptimizer.get_optimized_completed_services_count(
            start_date=today,
            end_date=today
        )
        
        # Get this month's stats
        month_start = today.replace(day=1)
        month_completed = ReportOptimizer.get_optimized_completed_services_count(
            start_date=month_start,
            end_date=today
        )
        
        # Get this week's stats
        week_start = today - timedelta(days=today.weekday())
        week_completed = ReportOptimizer.get_optimized_completed_services_count(
            start_date=week_start,
            end_date=today
        )
        
        return Response({
            'today_completed': today_completed,
            'week_completed': week_completed,
            'month_completed': month_completed,
            'date': today.isoformat()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'An error occurred while getting quick stats: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

