from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _


def home(request):
    """
    View simples para demonstrar a funcionalidade de internacionalização.
    """
    welcome_message = _("Bem-vindo ao Personal Trainer App")
    description = _("Plataforma completa para personal trainers gerenciarem seus negócios")
    
    context = {
        'welcome_message': welcome_message,
        'description': description,
    }
    
    return render(request, 'core/home.html', context)


def language_test(request):
    """
    View de teste para verificar se as traduções estão funcionando.
    """
    messages = [
        _("Bem-vindo ao Personal Trainer App"),
        _("Plataforma completa para personal trainers gerenciarem seus negócios"),
        _("Gestão de Clientes"),
        _("Avaliação Física Digital"),
        _("Agendamento Inteligente"),
        _("Planos de Treino"),
    ]
    
    html_content = "<h1>" + _("Teste de Internacionalização") + "</h1>"
    html_content += "<ul>"
    for message in messages:
        html_content += f"<li>{message}</li>"
    html_content += "</ul>"
    
    return HttpResponse(html_content)

