# ADR - Architectural Decision Record

**Projeto:** TechBazar — Marketplace de Eletrônicos Usados
**Data:** 2026-05-05
**Status:** Aprovado

---

## 1. Contexto

O TechBazar é um marketplace simplificado para compra e venda de eletrônicos usados (estilo OLX/Mercado Livre enxuto). O MVP precisa contemplar:

- Cadastro e autenticação de usuários (compradores e vendedores)
- Listagem e busca de produtos
- Carrinho de compras
- Fluxo de checkout

O sistema deve ser simples de desenvolver, fácil de manter e ter um time-to-market reduzido, dado que se trata de um projeto avaliativo com prazo curto.

---

## 2. Decisão

Adotaremos uma arquitetura de **Monólito Modular em Django (Python)**, separando o sistema em apps Django bem delimitados por contexto de negócio.

### 2.1 Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Backend | **Django 5.x** + Django REST Framework | Framework "batteries included", admin pronto, ORM robusto |
| Linguagem | **Python 3.12+** | Sintaxe clara, vasto ecossistema |
| Banco de Dados | **PostgreSQL 16** | Confiável, escalável, suporte a JSON e full-text search |
| Autenticação | **Django Auth** + **JWT (SimpleJWT)** | Auth nativo robusto, JWT para a API |
| Frontend | **HTML + Tailwind CSS** (templates Django) | Rápido para o MVP; pode evoluir para SPA depois |
| Cache/Sessão | **Redis** | Sessões, carrinho temporário e cache de queries |
| Storage de Imagens | **AWS S3** (ou local em dev) via `django-storages` | Imagens de produtos fora do servidor de aplicação |
| Containerização | **Docker + Docker Compose** | Ambientes reprodutíveis |
| CI/CD | **GitHub Actions** | Integração nativa com o repositório |
| Hospedagem | **Render** ou **Railway** | Deploy simples para projetos Django |

### 2.2 Estrutura Modular (Apps Django)

```
techbazar/
├── apps/
│   ├── accounts/      # Usuários, autenticação, perfis
│   ├── catalog/       # Produtos, categorias, busca
│   ├── cart/          # Carrinho de compras
│   ├── orders/        # Pedidos, checkout
│   └── core/          # Utilitários compartilhados
├── config/            # settings, urls, wsgi
├── templates/         # Templates HTML
├── static/            # CSS, JS, imagens
└── manage.py
```

Cada app tem responsabilidade única e se comunica com os outros via interfaces explícitas (services/signals), nunca acessando models de outro app diretamente em views.

---

## 3. Alternativas Consideradas

| Alternativa | Por que NÃO foi escolhida |
|---|---|
| **Microsserviços** | Complexidade desnecessária para um MVP; overhead de infra |
| **Serverless (AWS Lambda)** | Curva de aprendizado maior; cold starts; vendor lock-in |
| **Node.js + Express** | Exige montar mais peças manualmente (auth, admin, ORM) |
| **Next.js Full-stack** | Ótimo, mas o time tem mais familiaridade com Python/Django |

---

## 4. Consequências

### Positivas
- Deploy e desenvolvimento rápidos
- Django Admin pronto facilita gestão de produtos/usuários
- Time-to-market reduzido para o MVP
- Escalabilidade vertical adequada para o estágio atual
- Migração futura para microsserviços é viável (apps já estão modularizados)

### Negativas / Trade-offs
- Escalabilidade horizontal exige mais cuidado (sticky sessions, etc.)
- Acoplamento dentro do monólito precisa ser disciplinado
- Python tem performance inferior a Go/Rust em CPU-bound (não é o caso aqui)

---

## 5. Próximos Passos

1. Criar repositório e estrutura inicial do projeto Django
2. Modelar entidades (ver `DIAGRAMAS.md`)
3. Implementar app `accounts` (cadastro/login)
4. Implementar app `catalog` (CRUD de produtos + busca)
5. Implementar app `cart` e `orders`
6. Configurar pipeline CI/CD

---

**Autores:** Equipe TechBazar
**Revisão:** A cada nova feature significativa
