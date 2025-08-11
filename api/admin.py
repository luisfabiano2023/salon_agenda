from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Professional, Client, ServiceType, Appointment, Receptionist


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone',)}),
    )


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'phone', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'cpf', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'phone', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'cpf', 'email')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'duration_minutes', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'professional', 'service_type', 'scheduled_date', 'scheduled_time', 'status', 'price')
    list_filter = ('status', 'scheduled_date', 'created_at')
    search_fields = ('client__name', 'professional__name', 'service_type__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'scheduled_date'


@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'hire_date', 'is_active')
    list_filter = ('is_active', 'hire_date')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'employee_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
