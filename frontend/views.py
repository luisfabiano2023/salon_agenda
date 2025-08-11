from django.shortcuts import render


def login_page(request):
    """Login page for receptionists"""
    return render(request, 'frontend/login.html')


def dashboard(request):
    """Main dashboard for receptionists"""
    return render(request, 'frontend/dashboard.html')


def clients(request):
    """Client management page"""
    return render(request, 'frontend/clients.html')


def professionals(request):
    """Professional management page"""
    return render(request, 'frontend/professionals.html')


def services(request):
    """Service type management page"""
    return render(request, 'frontend/services.html')


def appointments(request):
    """Appointment management page"""
    return render(request, 'frontend/appointments.html')



def reports(request):
    """Service reports and analytics page"""
    return render(request, 'frontend/reports.html')

