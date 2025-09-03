[![CI/CD Pipeline](https://github.com/tramontano/personal-trainer/actions/workflows/ci.yml/badge.svg)](https://github.com/tramontano/personal-trainer/actions/workflows/ci.yml)
# Personal Trainer App - Plataforma Open-Source para Personal Trainers

Uma plataforma completa e open-source para personal trainers independentes gerenciarem seus negócios, com foco em musculação e treinamento funcional. Inspirada no Exercise.com, desenvolvida com Django e PostgreSQL.

## Visão Geral

Esta plataforma open-source oferece uma solução completa para personal trainers independentes, especialmente focada em:

- **Público-Alvo**: Personal trainers independentes no Brasil
- **Especialização**: Musculação e treinamento funcional
- **Modelo**: Open-source com serviços profissionais opcionais
- **Escalabilidade**: Projetado para até 200 usuários iniciais

### Funcionalidades Principais

- **Gestão de Clientes**: Perfis detalhados, histórico médico, objetivos
- **Avaliação Física Digital**: Anamnese, medidas, fotos de progresso, cálculos automáticos
- **Agendamento Inteligente**: Calendário integrado, sincronização com Google Calendar
- **Planos de Treino**: Biblioteca especializada em musculação e funcional
- **Precificação Flexível**: Cada personal trainer define valores individuais por cliente
- **Aplicativo Mobile**: Apps nativos para trainers e clientes
- **Integrações**: WhatsApp, Instagram, Google Calendar
- **Internacionalização**: Português, Inglês e Espanhol
- **Analytics**: Relatórios de negócio, métricas de performance

## Tecnologias

- **Backend**: Django 4.2+ com Django REST Framework
- **Banco de Dados**: PostgreSQL 14+
- **Cache**: Redis
- **Pagamentos**: Stripe
- **Notificações**: Celery + Redis
- **Deploy**: Docker + Docker Compose
- **Monitoramento**: New Relic / DataDog

## Pré-requisitos

- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Node.js 16+ (para frontend)
- Docker (opcional)

## Instalação

### Desenvolvimento Local

1. **Clone o repositório**
```bash
git clone https://github.com/tramontano/personal-trainer-app.git
cd personal-trainer-app
```

2. **Configure o ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements/development.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

### Docker (Recomendado)

```bash
docker-compose up -d
```

## Estrutura do Projeto

```
personal-trainer-app/
├── apps/
│   ├── core/              # Configurações base e utilitários
│   ├── authentication/    # Sistema de autenticação
│   ├── users/            # Gestão de usuários e perfis
│   ├── business/         # Agendamentos e calendário
│   ├── workouts/         # Treinos e exercícios
│   ├── payments/         # Processamento de pagamentos
│   ├── marketing/        # CRM e campanhas
│   ├── analytics/        # Relatórios e métricas
│   ├── notifications/    # Sistema de notificações
│   └── api/             # Endpoints da API REST
├── config/
│   ├── settings/        # Configurações do Django
│   ├── urls.py         # URLs principais
│   └── wsgi.py         # WSGI configuration
├── requirements/        # Dependências por ambiente
├── docs/               # Documentação
├── tests/              # Testes automatizados
└── docker-compose.yml  # Configuração Docker
```

## Configuração

### Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados
DB_NAME=personal_trainer_db
DB_USER=postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha

# SMS (Twilio)
TWILIO_ACCOUNT_SID=sua-account-sid
TWILIO_AUTH_TOKEN=seu-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

## Testes

Execute todos os testes:
```bash
python manage.py test
```

Execute testes com cobertura:
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## API Documentation

A documentação da API está disponível em:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

### Principais Endpoints

#### Autenticação
- `POST /api/auth/register/` - Registro de usuário
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout

#### Usuários
- `GET /api/users/profile/` - Perfil do usuário
- `PUT /api/users/profile/` - Atualizar perfil
- `GET /api/trainers/` - Lista de trainers
- `GET /api/clients/` - Lista de clientes

#### Agendamentos
- `GET /api/appointments/` - Lista de agendamentos
- `POST /api/appointments/` - Criar agendamento
- `PUT /api/appointments/{id}/` - Atualizar agendamento
- `DELETE /api/appointments/{id}/` - Cancelar agendamento

#### Treinos
- `GET /api/workout-plans/` - Planos de treino
- `POST /api/workout-plans/` - Criar plano
- `GET /api/exercises/` - Biblioteca de exercícios
- `POST /api/workout-sessions/` - Registrar sessão

#### Pagamentos
- `POST /api/payments/create-intent/` - Criar intenção de pagamento
- `POST /api/payments/confirm/` - Confirmar pagamento
- `GET /api/payments/history/` - Histórico de pagamentos

## Deploy

### Produção com Docker

1. **Configure as variáveis de produção**
```bash
cp .env.production.example .env.production
```

2. **Execute o deploy**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Deploy Manual

1. **Configure o servidor**
```bash
# Instale as dependências do sistema
sudo apt update
sudo apt install python3-pip postgresql redis-server nginx

# Configure o PostgreSQL
sudo -u postgres createdb personal_trainer_db
sudo -u postgres createuser --interactive
```

2. **Deploy da aplicação**
```bash
# Clone e configure
git clone https://github.com/tramontano/personal-trainer-app.git
cd personal-trainer-app
pip install -r requirements/production.txt

# Configure o banco
python manage.py migrate
python manage.py collectstatic

# Configure o Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Monitoramento

### Métricas Importantes

- **Performance**: Tempo de resposta da API < 200ms
- **Disponibilidade**: Uptime > 99.9%
- **Erros**: Taxa de erro < 0.1%
- **Usuários**: Usuários ativos diários/mensais

### Logs

Os logs são estruturados em JSON e incluem:
- Requests da API
- Erros de aplicação
- Eventos de negócio
- Métricas de performance

## Contribuição

1. **Fork o projeto**
2. **Crie uma branch para sua feature** (`git checkout -b feature/AmazingFeature`)
3. **Commit suas mudanças** (`git commit -m 'Add some AmazingFeature'`)
4. **Push para a branch** (`git push origin feature/AmazingFeature`)
5. **Abra um Pull Request**

### Padrões de Código

- Siga o PEP 8 para Python
- Use type hints quando possível
- Escreva testes para novas funcionalidades
- Mantenha cobertura de testes > 80%
- Use docstrings para funções e classes

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Roadmap

Veja nosso [roadmap detalhado](docs/roadmap.md) para conhecer as próximas funcionalidades e melhorias planejadas.

## Status do Projeto

![Build Status](https://img.shields.io/github/workflow/status/tramontano/personal-trainer-app/CI)
![Coverage](https://img.shields.io/codecov/c/github/tramontano/personal-trainer-app)
![License](https://img.shields.io/github/license/tramontano/personal-trainer-app)
![Version](https://img.shields.io/github/v/release/tramontano/personal-trainer-app)

---

**Desenvolvido com ❤️ pela comunidade**

