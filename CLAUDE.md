# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository

This is the `techbazar-docs` repository — Django + DRF marketplace de eletrônicos usados.

## Build & Run

```bash
# Ativar venv
.venv\Scripts\Activate.ps1  # Windows

# Servidor de desenvolvimento
python manage.py runserver

# Testes
pytest                          # todos os testes
pytest tests/test_e2e.py -v     # E2E (requer servidor rodando em :8000)

# Migrações
python manage.py makemigrations
python manage.py migrate

# Seed de produtos
python manage.py seed_products
```

## Convenções do projeto

- Apps ficam em `apps/` — nunca na raiz
- Testes de integração/API em `tests/`; testes de modelo em `apps/<app>/tests.py`
- Seletores nos testes E2E: **apenas** `data-testid` ou texto — nunca classes CSS utilitárias (Tailwind)
- Commits seguem Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`

## Workflow de PR — obrigatório

**Antes de abrir qualquer Pull Request**, sempre atualizar `docs/CHANGELOG.md`:

1. Adicionar uma nova seção no **topo** do arquivo (acima das demais)
2. Seguir o formato existente: branch, data, commit, tabela de entregáveis e lista do que mudou
3. Commitar a atualização do changelog junto com os demais commits da branch

Exemplo de seção:
```markdown
## PR #N — `feature/nome-da-branch` → `main` · YYYY-MM-DD
**O que mudou:**
- descrição resumida das mudanças
```
