# Sistema de Gestão para Salões de Beleza

Este projeto é um sistema completo para gestão de salões de beleza, incluindo funcionalidades para agendamento de serviços, gerenciamento de clientes, profissionais e tipos de serviço, além de relatórios e métricas de desempenho.  

O backend foi desenvolvido em **Django** com suporte a **JWT Authentication**, e o frontend consome a API REST disponibilizada.

---

## 📦 Instalação

1. **Instalar as dependências do Python:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Aplicar as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

3. **Criar um superusuário (conta de recepcionista):**
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções no terminal.  
    Para testes, você pode usar:
    - Email: `admin@salon.com`
    - Senha: `admin123` (ou a senha de sua preferência)

4. **Gerar dados de teste (opcional, para testes de performance):**
    ```bash
    python create_test_data.py
    ```
    Este script cria aproximadamente 3.000 agendamentos, além de clientes, profissionais e tipos de serviço.

---

## 🚀 Executando a Aplicação

1. **Iniciar o servidor de desenvolvimento Django:**
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

2. **Acessar no navegador:**
    ```
    http://127.0.0.1:8000
    ```
    Você será redirecionado para a página de login.  
    Use as credenciais do superusuário criado anteriormente.

---

## 🔑 Rotas da API

Todas as rotas da API requerem **JWT Authentication**.

### Authentication
- `POST /api/auth/login/`: Authenticate user and get JWT tokens.  
  **Request Body**: `{"email": "your_email@example.com", "password": "your_password"}`  
  **Response**: `{"access": "jwt_access_token", "refresh": "jwt_refresh_token"}`
- `POST /api/auth/refresh/`: Refresh JWT access token using refresh token.
- `POST /api/auth/logout/`: Invalidate JWT tokens.

### User Management
- `GET /api/users/`: List all users.
- `GET /api/users/{id}/`: Retrieve a specific user.
- `POST /api/users/`: Create a new user.
- `PUT /api/users/{id}/`: Update an existing user.
- `DELETE /api/users/{id}/`: Delete a user.

### Professional Management
- `GET /api/professionals/`: List all professionals.
- `GET /api/professionals/{id}/`: Retrieve a specific professional.
- `POST /api/professionals/`: Create a new professional.
- `PUT /api/professionals/{id}/`: Update an existing professional.
- `DELETE /api/professionals/{id}/`: Delete a professional.

### Client Management
- `GET /api/clients/`: List all clients.
- `GET /api/clients/{id}/`: Retrieve a specific client.
- `POST /api/clients/`: Create a new client.
- `PUT /api/clients/{id}/`: Update an existing client.
- `DELETE /api/clients/{id}/`: Delete a client.

### Service Type Management
- `GET /api/service-types/`: List all service types.
- `GET /api/service-types/{id}/`: Retrieve a specific service type.
- `POST /api/service-types/`: Create a new service type.
- `PUT /api/service-types/{id}/`: Update an existing service type.
- `DELETE /api/service-types/{id}/`: Delete a service type.

### Appointment Management
- `GET /api/appointments/`: List all appointments.
- `GET /api/appointments/{id}/`: Retrieve a specific appointment.
- `POST /api/appointments/`: Create a new appointment.
- `PUT /api/appointments/{id}/`: Update an existing appointment.
- `DELETE /api/appointments/{id}/`: Delete an appointment.

### Reporting Endpoints
- `GET /api/reports/completed-services/`: Get a detailed report of completed services.  
  **Query Params**: `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD), `professional_id` (UUID), `service_type_id` (UUID)
- `GET /api/reports/performance-metrics/`: Get overall salon performance metrics.  
  **Query Params**: `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD)
- `GET /api/reports/top-services/`: Get a list of top services by completion count.  
  **Query Params**: `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD), `limit` (int, default 10)
- `GET /api/reports/professional-performance/`: Get performance metrics for each professional.  
  **Query Params**: `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD)
- `GET /api/reports/quick-stats/`: Get quick statistics for the dashboard (today, week, month completed services).

---

## 🌐 Rotas do Frontend

- `/`: Dashboard page.
- `/login/`: Login page.
- `/clients/`: Client management page.
- `/professionals/`: Professional management page.
- `/services/`: Service type management page.
- `/appointments/`: Appointment management page.
- `/reports/`: Service reports and analytics page.
