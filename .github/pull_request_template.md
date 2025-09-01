---
name: Pull Request Template
about: Template for new pull requests
title: 
labels: [needs review]
assignees: 
---

## Descrição

Descreva brevemente as mudanças implementadas neste Pull Request.

## Tipo de Mudança

- [ ] Bug fix (mudança que corrige um problema)
- [ ] Nova feature (mudança que adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação (mudanças na documentação)
- [ ] Refatoração (nenhuma mudança funcional ou correção de bug)
- [ ] Estilo (formatação, semicolons ausentes, etc.)
- [ ] Teste (adição de testes ausentes ou correção de testes existentes)
- [ ] Build (mudanças que afetam o sistema de build ou dependências externas)
- [ ] CI/CD (mudanças nos arquivos e scripts de CI/CD)

## Motivação e Contexto

Explique por que esta mudança é necessária e qual problema ela resolve. Forneça contexto adicional, se aplicável.

## Como Testar

Descreva os passos para testar as mudanças. Inclua casos de teste específicos e configurações necessárias.

```bash
# Exemplo de comandos para testar
python manage.py test apps.your_app.tests.YourTestClass
```

## Checklist

- [ ] Meu código segue os padrões de estilo do projeto (PEP 8, Black, isort).
- [ ] Meus commits seguem as convenções de mensagens do projeto (Conventional Commits).
- [ ] Adicionei testes que comprovam que minha correção é eficaz ou que minha feature funciona.
- [ ] Os testes unitários e de integração passam localmente com minhas mudanças.
- [ ] Fiz as mudanças correspondentes na documentação.
- [ ] Minhas mudanças não introduzem novos warnings.
- [ ] Resolvi todos os conflitos de merge.

## Issues Relacionadas

Closes #[número da issue]

## Screenshots (Opcional)

Se aplicável, adicione screenshots para ajudar a explicar as mudanças visuais.

## Deploy

Este PR requer deploy no ambiente de produção? Se sim, quais passos adicionais são necessários?

## Revisores

@github_username1 @github_username2


