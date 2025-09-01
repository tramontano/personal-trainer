# Guia de Contribuição

Obrigado por considerar contribuir para o Personal Trainer App! Este documento fornece diretrizes para contribuir com o projeto.

## Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Melhorias](#sugerindo-melhorias)

## Código de Conduta

Este projeto adere ao [Código de Conduta do Contributor Covenant](CODE_OF_CONDUCT.md). Ao participar, você deve seguir este código.

## Como Contribuir

Existem várias maneiras de contribuir:

### Reportando Bugs
- Use o template de issue para bugs
- Inclua informações detalhadas sobre o ambiente
- Forneça passos para reproduzir o problema
- Inclua logs relevantes

### Sugerindo Melhorias
- Use o template de issue para feature requests
- Explique claramente o problema que a feature resolve
- Descreva a solução proposta
- Considere alternativas

### Contribuindo com Código
- Fork o repositório
- Crie uma branch para sua feature
- Implemente as mudanças
- Adicione testes
- Submeta um pull request

## Configuração do Ambiente

### Pré-requisitos
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Git

### Setup Local

1. **Fork e clone o repositório**
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
# Edite o arquivo .env conforme necessário
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Execute os testes**
```bash
python manage.py test
```

### Setup com Docker

```bash
docker-compose up -d
```

## Padrões de Código

### Python/Django

#### Estilo de Código
- Siga o [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) para formatação
- Use [isort](https://isort.readthedocs.io/) para imports
- Use [flake8](https://flake8.pycqa.org/) para linting

#### Configuração de Ferramentas

**Black**
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
```

**isort**
```toml
# pyproject.toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

**flake8**
```ini
# setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = migrations
```

#### Convenções de Nomenclatura

**Classes**
```python
class PersonalTrainer(models.Model):
    pass

class WorkoutPlanSerializer(serializers.ModelSerializer):
    pass

class AppointmentViewSet(viewsets.ModelViewSet):
    pass
```

**Funções e Variáveis**
```python
def create_workout_plan():
    pass

def calculate_bmi(weight, height):
    pass

user_profile = get_user_profile()
workout_sessions = WorkoutSession.objects.all()
```

**Constantes**
```python
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_SESSION_DURATION = 60  # minutes
USER_TYPE_CHOICES = [
    ('trainer', 'Personal Trainer'),
    ('client', 'Client'),
]
```

#### Type Hints
Use type hints sempre que possível:

```python
from typing import List, Optional, Dict, Any
from django.http import HttpRequest, HttpResponse

def get_user_workouts(user_id: int) -> List[Dict[str, Any]]:
    """Retorna lista de treinos do usuário."""
    pass

def process_payment(amount: float, currency: str = 'BRL') -> Optional[str]:
    """Processa pagamento e retorna ID da transação."""
    pass
```

#### Docstrings
Use docstrings no formato Google:

```python
def calculate_workout_intensity(
    heart_rate: int, 
    max_heart_rate: int
) -> float:
    """Calcula a intensidade do treino baseada na frequência cardíaca.
    
    Args:
        heart_rate: Frequência cardíaca atual em BPM
        max_heart_rate: Frequência cardíaca máxima em BPM
        
    Returns:
        Intensidade do treino como percentual (0.0 a 1.0)
        
    Raises:
        ValueError: Se heart_rate for maior que max_heart_rate
    """
    if heart_rate > max_heart_rate:
        raise ValueError("Heart rate cannot exceed max heart rate")
    
    return heart_rate / max_heart_rate
```

### Django Específico

#### Models
```python
class WorkoutPlan(models.Model):
    """Plano de treino criado por um personal trainer."""
    
    name = models.CharField(max_length=200, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    trainer = models.ForeignKey(
        'users.PersonalTrainer',
        on_delete=models.CASCADE,
        related_name='workout_plans'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Plano de Treino"
        verbose_name_plural = "Planos de Treino"
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"{self.name} - {self.trainer.user.get_full_name()}"
```

#### Serializers
```python
class WorkoutPlanSerializer(serializers.ModelSerializer):
    """Serializer para planos de treino."""
    
    trainer_name = serializers.CharField(
        source='trainer.user.get_full_name', 
        read_only=True
    )
    exercises_count = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'name', 'description', 'trainer_name', 
            'exercises_count', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_exercises_count(self, obj: WorkoutPlan) -> int:
        """Retorna o número de exercícios no plano."""
        return obj.exercises.count()
```

#### Views
```python
class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar planos de treino."""
    
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['trainer', 'created_at']
    search_fields = ['name', 'description']
    
    def get_queryset(self) -> QuerySet[WorkoutPlan]:
        """Retorna queryset filtrado por usuário."""
        user = self.request.user
        if hasattr(user, 'personaltrainer'):
            return WorkoutPlan.objects.filter(trainer=user.personaltrainer)
        return WorkoutPlan.objects.filter(
            trainer__clients__user=user
        ).distinct()
```

### Testes

#### Estrutura de Testes
```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class WorkoutPlanModelTest(TestCase):
    """Testes para o modelo WorkoutPlan."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            email='trainer@example.com',
            password='testpass123'
        )
        self.trainer = PersonalTrainer.objects.create(
            user=self.user,
            business_name='Test Gym'
        )
    
    def test_workout_plan_creation(self):
        """Testa a criação de um plano de treino."""
        plan = WorkoutPlan.objects.create(
            name='Treino A',
            description='Treino para iniciantes',
            trainer=self.trainer
        )
        
        self.assertEqual(plan.name, 'Treino A')
        self.assertEqual(plan.trainer, self.trainer)
        self.assertTrue(plan.created_at)

class WorkoutPlanAPITest(APITestCase):
    """Testes para a API de planos de treino."""
    
    def setUp(self):
        """Configuração inicial para os testes da API."""
        self.user = User.objects.create_user(
            email='trainer@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_workout_plan(self):
        """Testa a criação de plano via API."""
        data = {
            'name': 'Novo Treino',
            'description': 'Descrição do treino'
        }
        
        response = self.client.post('/api/workout-plans/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Novo Treino')
```

#### Factories
Use factory_boy para criar objetos de teste:

```python
import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """Factory para criar usuários de teste."""
    
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class PersonalTrainerFactory(factory.django.DjangoModelFactory):
    """Factory para criar personal trainers de teste."""
    
    class Meta:
        model = PersonalTrainer
    
    user = factory.SubFactory(UserFactory)
    business_name = factory.Faker('company')
    bio = factory.Faker('text')
```

## Processo de Pull Request

### Antes de Submeter

1. **Certifique-se que os testes passam**
```bash
python manage.py test
```

2. **Execute o linting**
```bash
flake8 .
black --check .
isort --check-only .
```

3. **Verifique a cobertura de testes**
```bash
coverage run --source='.' manage.py test
coverage report
```

### Criando o Pull Request

1. **Crie uma branch descritiva**
```bash
git checkout -b feature/add-workout-tracking
git checkout -b fix/payment-validation-bug
git checkout -b docs/update-api-documentation
```

2. **Faça commits atômicos com mensagens claras**
```bash
git commit -m "feat: add workout progress tracking

- Add WorkoutSession model
- Implement progress calculation
- Add API endpoints for session logging
- Include tests for new functionality

Closes #123"
```

3. **Mantenha o histórico limpo**
```bash
# Rebase antes de submeter
git rebase main
```

### Template de Pull Request

```markdown
## Descrição
Breve descrição das mudanças implementadas.

## Tipo de Mudança
- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova feature (mudança que adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação

## Como Testar
1. Passos para testar as mudanças
2. Casos de teste específicos
3. Configurações necessárias

## Checklist
- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Mudanças foram testadas localmente
- [ ] Não há conflitos de merge

## Issues Relacionadas
Closes #123
Related to #456
```

## Reportando Bugs

### Template de Bug Report

```markdown
## Descrição do Bug
Uma descrição clara e concisa do que é o bug. Qual comportamento inesperado você observou?

## Passos para Reproduzir
Passos para reproduzir o bug:
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

## Comportamento Esperado
Uma descrição clara e concisa do que você esperava que acontecesse.

## Comportamento Atual
Uma descrição clara e concisa do que realmente aconteceu.

## Screenshots
Se aplicável, adicione screenshots para ajudar a explicar o problema.

## Ambiente
- Sistema Operacional: [e.g. Windows 10, macOS Ventura, Ubuntu 22.04]
- Versão do Projeto: [e.g. v1.0.0, main branch, commit hash]
- Python: [e.g. 3.9.7]
- Django: [e.g. 4.2.7]
- Navegador: [e.g. Chrome 120, Firefox 119, Safari 17]

## Informações Adicionais
Qualquer outra informação relevante sobre o problema, como logs de erro, mensagens do console, ou contexto adicional que possa ser útil para a depuração.

'''
# Cole logs de erro aqui, se houver
'''
```

## Sugerindo Melhorias

### Template de Feature Request

```markdown
## Resumo da Feature
Uma descrição clara e concisa da funcionalidade que você gostaria de ver implementada.

## Problema que Resolve
Descreva o problema que esta nova funcionalidade resolveria ou a necessidade que ela atenderia. Por que esta funcionalidade é importante?

## Solução Proposta
Descreva em detalhes como você imagina que esta funcionalidade funcionaria. Inclua:
- **Funcionalidades Específicas**: Quais ações o usuário poderia realizar?
- **Fluxo de Usuário**: Como o usuário interagiria com a nova funcionalidade?
- **Integrações**: Se houver, com quais sistemas ou outras funcionalidades ela se integraria?
- **Impacto Esperado**: Como esta funcionalidade beneficiaria os usuários ou o projeto?

## Alternativas Consideradas
Você considerou alguma solução alternativa ou abordagens diferentes para resolver o mesmo problema? Se sim, quais e por que a solução proposta é preferível?

## Informações Adicionais
Adicione qualquer contexto adicional ou screenshots/mockups que possam ajudar a entender melhor a sua sugestão.
- Link para mockups ou wireframes (se houver)
- Link para exemplos em outras plataformas (se houver)
- Qualquer outra informação relevante
```

## Recursos Adicionais

- [Documentação do Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

## Precisa de Ajuda?

- Abra uma issue com a tag `question`
- Entre em contato via email: tramontanophillipe@gmail.com
- Consulte a documentação do projeto

Obrigado por contribuir! 🎉

