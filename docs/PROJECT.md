# Estrutura Técnica do Projeto Django - Personal Trainer App

## Arquitetura Geral

### Stack Tecnológico
- **Backend**: Django 4.2+ com Django REST Framework
- **Banco de Dados**: PostgreSQL 14+
- **Autenticação**: Django Authentication + JWT
- **Cache**: Redis
- **Armazenamento de Arquivos**: AWS S3 ou similar
- **Processamento de Pagamentos**: Stripe
- **Notificações**: Celery + Redis
- **Deploy**: Docker + Docker Compose

## Estrutura de Apps Django

### 1. Core App (core/)
- Configurações base
- Modelos abstratos
- Utilitários comuns
- Middleware customizado

### 2. Authentication App (authentication/)
- Modelos de usuário customizados
- Autenticação JWT
- Permissões e grupos
- Recuperação de senha

### 3. Users App (users/)
- Perfis de usuário (Personal Trainer, Cliente)
- Gerenciamento de perfis
- Configurações de usuário

### 4. Business App (business/)
- Agendamentos
- Calendário
- Disponibilidade
- Configurações de negócio

### 5. Workouts App (workouts/)
- Exercícios
- Planos de treino
- Sessões de treino
- Progresso do cliente

### 6. Payments App (payments/)
- Processamento de pagamentos
- Assinaturas
- Faturas
- Comissões

### 7. Marketing App (marketing/)
- CRM
- Campanhas de email/SMS
- Leads
- Automações

### 8. Analytics App (analytics/)
- Relatórios
- Métricas de negócio
- Dashboard

### 9. Notifications App (notifications/)
- Sistema de notificações
- Templates de mensagens
- Histórico de notificações

### 10. API App (api/)
- Serializers
- ViewSets
- Endpoints da API REST

## Modelos de Dados Principais

### User (authentication/models.py)
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### PersonalTrainer (users/models.py)
```python
class PersonalTrainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    bio = models.TextField()
    specializations = models.ManyToManyField('Specialization')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
```

### Client (users/models.py)
```python
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE)
    goals = models.TextField()
    fitness_level = models.CharField(max_length=50)
    medical_conditions = models.TextField(blank=True)
```

### Appointment (business/models.py)
```python
class Appointment(models.Model):
    trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    duration = models.DurationField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
```

### WorkoutPlan (workouts/models.py)
```python
class WorkoutPlan(models.Model):
    trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration_weeks = models.IntegerField()
    is_active = models.BooleanField(default=True)
```

### Exercise (workouts/models.py)
```python
class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    muscle_groups = models.ManyToManyField('MuscleGroup')
    equipment_needed = models.ManyToManyField('Equipment')
    difficulty_level = models.CharField(max_length=20)
```

### Payment (payments/models.py)
```python
class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    stripe_payment_id = models.CharField(max_length=200)
```

## Configurações do Django

### settings/base.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'celery',
    'core',
    'authentication',
    'users',
    'business',
    'workouts',
    'payments',
    'marketing',
    'analytics',
    'notifications',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

### settings/development.py
```python
from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

## API Endpoints

### Authentication
- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/refresh/
- POST /api/auth/logout/
- POST /api/auth/password-reset/

### Users
- GET /api/users/profile/
- PUT /api/users/profile/
- GET /api/trainers/
- GET /api/trainers/{id}/
- GET /api/clients/

### Business
- GET /api/appointments/
- POST /api/appointments/
- PUT /api/appointments/{id}/
- DELETE /api/appointments/{id}/
- GET /api/availability/
- POST /api/availability/

### Workouts
- GET /api/workout-plans/
- POST /api/workout-plans/
- GET /api/exercises/
- POST /api/workout-sessions/
- GET /api/progress/

### Payments
- POST /api/payments/create-intent/
- POST /api/payments/confirm/
- GET /api/payments/history/
- GET /api/subscriptions/

### Marketing
- GET /api/leads/
- POST /api/campaigns/
- GET /api/analytics/dashboard/

## Segurança

### Autenticação e Autorização
- JWT tokens com refresh
- Permissões baseadas em roles
- Rate limiting
- CORS configurado

### Validação de Dados
- Serializers do DRF
- Validação customizada
- Sanitização de inputs

### Proteção de Dados
- Criptografia de dados sensíveis
- HTTPS obrigatório em produção
- Backup automático do banco

## Performance

### Cache
- Redis para cache de sessões
- Cache de queries frequentes
- Cache de templates

### Otimizações
- Select_related e prefetch_related
- Índices no banco de dados
- Compressão de assets

### Monitoramento
- Logs estruturados
- Métricas de performance
- Alertas automáticos

