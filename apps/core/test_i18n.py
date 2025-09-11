import pytest
from django.test import Client
from django.utils import translation


@pytest.mark.django_db
class TestInternationalization:
    """
    Testes para verificar se a internacionalização está funcionando corretamente.
    """

    def test_default_language_is_portuguese(self, client: Client):
        """Testa se o idioma padrão é português brasileiro."""
        response = client.get('/')
        assert response.status_code == 200
        assert 'Bem-vindo ao Personal Trainer App' in response.content.decode()

    def test_english_translation(self, client: Client):
        """Testa se as traduções em inglês funcionam."""
        response = client.get('/en/')
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Welcome to Personal Trainer App' in content
        assert 'Main Features' in content
        assert 'Client Management' in content

    def test_spanish_translation(self, client: Client):
        """Testa se as traduções em espanhol funcionam."""
        response = client.get('/es/')
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Bienvenido a la App Entrenador Personal' in content
        assert 'Funcionalidades Principales' in content
        assert 'Gestión de Clientes' in content

    def test_language_test_view_portuguese(self, client: Client):
        """Testa a view de teste de idiomas em português."""
        response = client.get('/language-test/')
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Teste de Internacionalização' in content
        assert 'Bem-vindo ao Personal Trainer App' in content

    def test_language_test_view_english(self, client: Client):
        """Testa a view de teste de idiomas em inglês."""
        response = client.get('/en/language-test/')
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Internationalization Test' in content
        assert 'Welcome to Personal Trainer App' in content

    def test_language_test_view_spanish(self, client: Client):
        """Testa a view de teste de idiomas em espanhol."""
        response = client.get('/es/language-test/')
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Prueba de Internacionalización' in content
        assert 'Bienvenido a la App Entrenador Personal' in content

    def test_language_code_in_context(self, client: Client):
        """Testa se o código do idioma está disponível no contexto."""
        # Teste português
        response = client.get('/')
        assert 'pt-br' in response.content.decode()

        # Teste inglês
        response = client.get('/en/')
        assert 'en' in response.content.decode()

        # Teste espanhol
        response = client.get('/es/')
        assert 'es' in response.content.decode()

    def test_translation_activation(self):
        """Testa se a ativação manual de idiomas funciona."""
        # Ativar português
        translation.activate('pt-br')
        from django.utils.translation import gettext as _
        expected = "Bem-vindo ao Personal Trainer App"
        assert _("Bem-vindo ao Personal Trainer App") == expected

        # Ativar inglês
        translation.activate('en')
        from django.utils.translation import gettext as _
        expected = "Welcome to Personal Trainer App"
        assert _("Bem-vindo ao Personal Trainer App") == expected

        # Ativar espanhol
        translation.activate('es')
        from django.utils.translation import gettext as _
        expected = "Bienvenido a la App Entrenador Personal"
        assert _("Bem-vindo ao Personal Trainer App") == expected

        # Desativar
        translation.deactivate()
