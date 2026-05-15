# TechBazar

O marketplace honesto de eletronicos usados.

Este repositorio comecou como documentacao arquitetural e agora entrou na fase inicial de implementacao com Django.

## Sobre o projeto

TechBazar e um mini-projeto academico focado em um marketplace enxuto de compra e venda de eletronicos usados.

Escopo do MVP:

- Cadastro e autenticacao de usuarios
- Listagem e busca de produtos
- Carrinho de compras
- Fluxo de checkout

## Stack tecnologica

| Camada | Tecnologia |
|---|---|
| Backend | Django 6.x + Django REST Framework |
| Linguagem | Python 3.14 (ambiente local atual) |
| Banco de Dados | PostgreSQL 16 (com fallback local para SQLite) |
| Frontend | HTML + Tailwind CSS |

Detalhes arquiteturais: [docs/ADR.md](docs/ADR.md)

## Estrutura atual

```
techbazar-docs/
├── apps/
│   ├── core/
│   └── catalog/
├── config/
├── docs/
│   ├── ADR.md
│   ├── erDiagram.md
│   ├── flowchart-TD.md
│   └── index.html
├── manage.py
├── requirements.txt
└── README.md
```

## O que ja foi implementado

Fase inicial de CRUD simplificado no app catalog:

- Projeto Django configurado
- App catalog com modelo Product
- Validacoes basicas de dominio
- Django Admin para Product
- API REST CRUD via DRF
- Busca por titulo/categoria e ordenacao
- Seed de dados para demo

Carrinho funcional simples:

- Carrinho por sessao (sem login obrigatorio)
- Adicao de item ao carrinho
- Atualizacao de quantidade
- Remocao de item
- Validacao de estoque disponivel

## Modelo Product (resumo)

Campos principais:

- seller
- title
- description
- price
- category
- condition
- image_url
- stock
- is_active
- created_at

Regras minimas:

- price deve ser maior que zero
- stock nao pode ser negativo
- produto inativo nao pode ser alterado por PUT/PATCH

## Setup local

### 1. Criar e ativar ambiente virtual

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Migrar banco

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Popular dados iniciais (opcional)

```powershell
python manage.py seed_products
```

### 5. Subir servidor

```powershell
python manage.py runserver
```

## Endpoints da API (CRUD inicial)

Base URL: /api/

- GET /api/products/
- POST /api/products/
- GET /api/products/{id}/
- PUT /api/products/{id}/
- PATCH /api/products/{id}/
- DELETE /api/products/{id}/

Filtros suportados na listagem:

- search: busca por title e category
- ordering: price, created_at, title

Exemplo:

- /api/products/?search=iphone
- /api/products/?ordering=price
- /api/products/?ordering=-created_at

## Endpoints da API (Carrinho simples)

Base URL: /api/cart/

- GET /api/cart/
- POST /api/cart/items/
- PATCH /api/cart/items/{item_id}/
- DELETE /api/cart/items/{item_id}/

Exemplo de payload para adicionar item:

```json
{
	"product_id": 1,
	"quantity": 2
}
```

## Testes

O projeto usa **pytest** com três camadas de testes:

| Tipo | Localização | O que cobre |
|------|------------|-------------|
| Unitários | `tests/test_cart.py` | Lógica em memória de `ShoppingCart` |
| Integração / API | `tests/test_api_products.py`, `tests/test_api_cart.py` | Endpoints REST via cliente HTTP |
| E2E (Playwright) | `tests/test_e2e.py` | Frontend `/app/` no Chromium headless |

### Rodar todos os testes (unitários + integração)

```powershell
pytest
```

### Rodar uma suíte específica

```powershell
pytest tests/test_cart.py          # unitários — ShoppingCart
pytest tests/test_api_products.py  # API de produtos
pytest tests/test_api_cart.py      # API do carrinho
pytest apps/catalog/tests.py       # testes de modelo (catalog)
pytest apps/cart/tests.py          # testes de modelo (cart)
```

### Rodar testes E2E (Playwright)

> **Pré-requisito:** servidor rodando em `http://localhost:8000`

```powershell
# 1ª vez — baixar o browser
playwright install chromium

# Rodar headless (padrão CI)
pytest tests/test_e2e.py -v

# Rodar com browser visível
pytest tests/test_e2e.py -v --headed
```

### Rodar com relatório de cobertura

```powershell
pytest --cov=apps --cov-report=term-missing
```

### Testes manuais de API (REST Client)

Abra `docs/techbazar-api.http` no VS Code com a extensão
[REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
e clique em **Send Request** em cada cenário. Requer servidor rodando em `:8000`.

## CI/CD

Foi adicionado pipeline no GitHub Actions em .github/workflows/ci.yml com:

- Instalacao de dependencias
- Execucao de migracoes
- Execucao de testes

Gatilhos:

- push em main e branches feature/**
- pull request para main

## Proximos passos

- Implementar app accounts (cadastro/login)
- Integrar autenticacao nas operacoes de catalog
- Iniciar app cart
- Iniciar app orders

## Licenca

Projeto academico sob licenca MIT.
