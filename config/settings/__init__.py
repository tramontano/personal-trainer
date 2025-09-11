"""
Configurações do Django organizadas por ambiente.
"""

from decouple import config

# Determina qual configuração usar baseado na variável de ambiente
ENVIRONMENT = config('DJANGO_ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *  # noqa: F403, F401
elif ENVIRONMENT == 'testing':
    from .testing import *  # noqa: F403, F401
else:
    from .development import *  # noqa: F403, F401
