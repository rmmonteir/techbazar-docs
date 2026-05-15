# CHANGELOG — TechBazar

Histórico resumido de cada PR mergeado na branch `main` e branches de feature ativas.

---

## [feature/hands-on-3-e2e-risco] — Em desenvolvimento · 2026-05-15

**Branch:** `feature/hands-on-3-e2e-risco` · **Commit:** `7c0aa4b`

Exercício Hands-on 3 da disciplina: testes E2E com Playwright, coleção REST Client e análise preditiva de risco de código.

| Entregável | Arquivo |
|-----------|---------|
| Testes E2E (Playwright Python) | `tests/test_e2e.py` — 10/10 passando |
| Coleção REST Client | `docs/techbazar-api.http` — 14 cenários |
| Análise de Risco | `docs/RISK_ANALYSIS.md` |

**O que mudou:**
- `docs/index.html` — URL da API corrigida para relativa; atributos `data-testid` adicionados em 5 elementos interativos (seletores estáveis para E2E)
- `config/urls.py` — rota `/app/` via `TemplateView` (frontend acessível pelo servidor Django)
- `config/settings.py` — diretório `docs/` adicionado ao `TEMPLATES DIRS`
- `requirements.txt` + `pyproject.toml` — `playwright`, `pytest-playwright`, `base_url` configurado

**Módulo de maior risco identificado:** `ShoppingCart.discount_amount` em `cart.py` (score 25 — CC=5 × FA=5)

---

## PR #3 — `caos` → `main` · 2026-05-12

**Commit de merge:** `13bcdb3` · **Arquivos alterados:** 2

PR de exercício para prática de revisão de código e resolução de conflitos Git.

**O que mudou:**
- `docs/index.html` — conflito Git intencional resolvido (marcadores `<<<<<<<` removidos, copy da hero section normalizada)
- `review.md` — criado com análise completa do PR: 2 bloqueadores identificados (conflito não resolvido no HTML; ausência de evolução funcional alinhada ao escopo arquitetural)

---

## PR #2 — `feature/frontend-api-integration` → `main` · 2026-05-11

**Commit de merge:** `c348879` · **Arquivos alterados:** 9

Integração do frontend estático com a API Django REST e adição da suíte de testes de API.

**O que mudou:**
- `docs/index.html` — refatoração completa: JS conectado à API real (`/api/products/`, `/api/cart/items/`); busca com debounce; filtro por categoria; contador de itens no carrinho; tratamento de erros de rede
- `config/settings.py` — `django-cors-headers` e `drf-spectacular` adicionados ao `INSTALLED_APPS`
- `requirements.txt` — `django-cors-headers` adicionado
- `pyproject.toml` — dependências de dev atualizadas
- `.github/workflows/ci.yml` — pipeline atualizado para rodar testes de API
- `tests/test_api_products.py` — criado: testes de integração para CRUD de produtos (listagem, busca, ordenação, validações)
- `tests/test_api_cart.py` — criado: testes de integração do carrinho (add/update/delete, validações de estoque e produto inativo)
- `tests/test_cart.py` — criado: testes unitários para `ShoppingCart` (`cart.py`)

---

## PR #1 — `feature/crud-inicial-catalog` → `main` · 2026-05-11

**Commit de merge:** `b2a8fcb` · **Arquivos alterados:** ~25

Implementação inicial do projeto: modelos, API REST, testes e CI/CD.

**O que mudou:**
- `apps/catalog/` — app `catalog` com modelo `Product`, `ProductViewSet` (CRUD completo), serializer com validações (preço > 0, inativo não editável), rotas DRF, admin, migrações
- `apps/cart/` — app `cart` com modelos `Cart` e `CartItem`, views (`CartDetailView`, `CartItemAddView`, `CartItemDetailView`), serializers, rotas, admin, migrações
- `apps/core/` — app base do projeto
- `config/` — `settings.py`, `urls.py`, `wsgi.py`, `asgi.py` configurados (DRF, drf-spectacular, sessões, CORS)
- `cart.py` — classe `ShoppingCart` em memória com suporte a desconto por threshold
- `manage.py`, `pyproject.toml`, `requirements.txt`, `.gitignore` — scaffolding do projeto
- `.github/workflows/ci.yml` — pipeline CI criado (lint + testes + cobertura)
- `README.md` — documentado com arquitetura, rotas e instruções de setup
- `.coverage` — relatório de cobertura incluído (100% em `cart.py`)

---

## Commits iniciais · antes do PR #1

| Data | Commit | Descrição |
|------|--------|-----------|
| 2026-05-11 | `70c3395` | Atualização de membros e papéis no README |
| 2026-05-11 | `9206b15` | Documentação inicial do projeto TechBazar |
| 2026-05-11 | `3b4363c` | Ajustes nos diagramas ER e de fluxo |
| 2026-05-11 | `794e106` | Arquivos de docs gerados (diagramas, ADR, diretrizes de IA) |
