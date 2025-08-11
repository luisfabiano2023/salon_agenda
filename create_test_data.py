#!/usr/bin/env python
"""
Script to create test data for performance testing.
This script will create thousands of appointments to test report performance.
"""

import os
import sys
import django
from datetime import datetime, timedelta, time
import random
from decimal import Decimal

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_agenda.settings')
django.setup()

from api.models import Client, Professional, ServiceType, Appointment


def create_test_data():
    """Create test data for performance testing"""
    
    print("Creating test data for performance testing...")
    
    # Create service types if they don't exist
    service_types = [
        {'name': 'Corte de Cabelo', 'description': 'Corte de cabelo feminino', 'base_price': Decimal('50.00'), 'duration_minutes': 60},
        {'name': 'Corte Masculino', 'description': 'Corte de cabelo masculino', 'base_price': Decimal('30.00'), 'duration_minutes': 45},
        {'name': 'Manicure', 'description': 'Manicure completa', 'base_price': Decimal('25.00'), 'duration_minutes': 45},
        {'name': 'Pedicure', 'description': 'Pedicure completa', 'base_price': Decimal('30.00'), 'duration_minutes': 60},
        {'name': 'Escova', 'description': 'Escova progressiva', 'base_price': Decimal('80.00'), 'duration_minutes': 120},
        {'name': 'Coloração', 'description': 'Coloração de cabelo', 'base_price': Decimal('120.00'), 'duration_minutes': 180},
        {'name': 'Hidratação', 'description': 'Hidratação capilar', 'base_price': Decimal('40.00'), 'duration_minutes': 90},
        {'name': 'Maquiagem', 'description': 'Maquiagem profissional', 'base_price': Decimal('60.00'), 'duration_minutes': 60},
        {'name': 'Sobrancelha', 'description': 'Design de sobrancelha', 'base_price': Decimal('20.00'), 'duration_minutes': 30},
        {'name': 'Massagem', 'description': 'Massagem relaxante', 'base_price': Decimal('70.00'), 'duration_minutes': 90},
    ]
    
    created_services = []
    for service_data in service_types:
        service, created = ServiceType.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        created_services.append(service)
        if created:
            print(f"Created service: {service.name}")
    
    # Create professionals if they don't exist
    professionals_data = [
        {'name': 'Maria Silva', 'cpf': '12345678901', 'phone': '+5511999999001', 'email': 'maria@salon.com', 'specialties': 'Cabelo, Coloração'},
        {'name': 'Ana Santos', 'cpf': '12345678902', 'phone': '+5511999999002', 'email': 'ana@salon.com', 'specialties': 'Manicure, Pedicure'},
        {'name': 'João Oliveira', 'cpf': '12345678903', 'phone': '+5511999999003', 'email': 'joao@salon.com', 'specialties': 'Corte Masculino'},
        {'name': 'Carla Ferreira', 'cpf': '12345678904', 'phone': '+5511999999004', 'email': 'carla@salon.com', 'specialties': 'Maquiagem, Sobrancelha'},
        {'name': 'Pedro Costa', 'cpf': '12345678905', 'phone': '+5511999999005', 'email': 'pedro@salon.com', 'specialties': 'Massagem'},
        {'name': 'Lucia Rodrigues', 'cpf': '12345678906', 'phone': '+5511999999006', 'email': 'lucia@salon.com', 'specialties': 'Hidratação, Escova'},
    ]
    
    created_professionals = []
    for prof_data in professionals_data:
        professional, created = Professional.objects.get_or_create(
            cpf=prof_data['cpf'],
            defaults=prof_data
        )
        created_professionals.append(professional)
        if created:
            print(f"Created professional: {professional.name}")
    
    # Create clients
    print("Creating clients...")
    clients_data = []
    for i in range(500):  # Create 500 clients
        client_data = {
            'name': f'Cliente {i+1}',
            'cpf': f'{12345678900 + i:011d}',
            'phone': f'+551199999{i+1000:04d}',
            'email': f'cliente{i+1}@email.com',
            'address': f'Rua {i+1}, {i+1}',
            'birth_date': datetime(1980 + (i % 40), 1 + (i % 12), 1 + (i % 28)).date(),
            'notes': f'Cliente número {i+1}',
        }
        clients_data.append(client_data)
    
    created_clients = []
    for client_data in clients_data:
        client, created = Client.objects.get_or_create(
            cpf=client_data['cpf'],
            defaults=client_data
        )
        created_clients.append(client)
        if created and len(created_clients) % 100 == 0:
            print(f"Created {len(created_clients)} clients...")
    
    print(f"Total clients created: {len(created_clients)}")
    
    # Create appointments
    print("Creating appointments...")
    
    # Generate appointments for the last 6 months
    start_date = datetime.now().date() - timedelta(days=180)
    end_date = datetime.now().date()
    
    statuses = ['scheduled', 'completed', 'cancelled', 'no_show']
    status_weights = [0.1, 0.7, 0.15, 0.05]  # 70% completed, 10% scheduled, 15% cancelled, 5% no-show
    
    appointments_created = 0
    current_date = start_date
    
    while current_date <= end_date:
        # Skip Sundays (assuming salon is closed)
        if current_date.weekday() == 6:
            current_date += timedelta(days=1)
            continue
        
        # Create 15-25 appointments per day
        daily_appointments = random.randint(15, 25)
        
        for _ in range(daily_appointments):
            # Random time between 8 AM and 6 PM
            hour = random.randint(8, 17)
            minute = random.choice([0, 30])
            appointment_time = time(hour, minute)
            
            # Random client, professional, and service
            client = random.choice(created_clients)
            professional = random.choice(created_professionals)
            service = random.choice(created_services)
            
            # Random status based on weights
            status = random.choices(statuses, weights=status_weights)[0]
            
            # Price variation (±20% from base price)
            price_variation = random.uniform(0.8, 1.2)
            price = service.base_price * Decimal(str(price_variation))
            price = price.quantize(Decimal('0.01'))
            
            try:
                appointment = Appointment.objects.create(
                    client=client,
                    professional=professional,
                    service_type=service,
                    scheduled_date=current_date,
                    scheduled_time=appointment_time,
                    duration_minutes=service.duration_minutes,
                    price=price,
                    status=status,
                    notes=f'Appointment created for testing - {status}'
                )
                appointments_created += 1
                
                if appointments_created % 1000 == 0:
                    print(f"Created {appointments_created} appointments...")
                    
            except Exception as e:
                # Skip if there's a conflict (same professional, date, time)
                continue
        
        current_date += timedelta(days=1)
    
    print(f"Total appointments created: {appointments_created}")
    print("Test data creation completed!")
    
    # Print summary statistics
    print("\n=== SUMMARY ===")
    print(f"Service Types: {ServiceType.objects.count()}")
    print(f"Professionals: {Professional.objects.count()}")
    print(f"Clients: {Client.objects.count()}")
    print(f"Total Appointments: {Appointment.objects.count()}")
    print(f"Completed Appointments: {Appointment.objects.filter(status='completed').count()}")
    print(f"Scheduled Appointments: {Appointment.objects.filter(status='scheduled').count()}")
    print(f"Cancelled Appointments: {Appointment.objects.filter(status='cancelled').count()}")
    print(f"No-show Appointments: {Appointment.objects.filter(status='no_show').count()}")


if __name__ == '__main__':
    create_test_data()

