# TechBazar 🛒⚡

> O marketplace honesto de eletrônicos usados.

TechBazar é um marketplace simplificado para compra e venda de eletrônicos usados (estilo OLX / Mercado Livre enxuto). Este repositório contém a documentação inicial, diagramação e mockup da home page do projeto.

---

## 📋 Sobre o Projeto

O TechBazar nasceu como um mini-projeto avaliativo focado em planejamento arquitetural, modelagem de banco de dados e prototipação visual. O MVP contempla:

- ✅ Cadastro e autenticação de usuários
- ✅ Listagem e busca de produtos
- ✅ Carrinho de compras
- ✅ Fluxo de checkout

---

## 🏗️ Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Django 5.x + Django REST Framework |
| Linguagem | Python 3.12+ |
| Banco de Dados | PostgreSQL 16 |
| Cache/Sessão | Redis |
| Frontend | HTML + Tailwind CSS |
| Storage | AWS S3 (django-storages) |
| Containerização | Docker + Docker Compose |
| CI/CD | GitHub Actions |

> Detalhes completos da decisão arquitetural em [`docs/ADR.md`](docs/ADR.md).

---

## 📁 Estrutura do Repositório

```
techbazar-docs/
├── docs/
│   ├── ADR.md          # Architectural Decision Record
│   └── DIAGRAMAS.md    # Diagramas ER e Fluxo (Mermaid)
├── index.html          # Mockup da home page
└── README.md
```

---

## 📐 Documentação

### Architectural Decision Record (ADR)
O arquivo [`docs/ADR.md`](docs/ADR.md) documenta:
- Contexto do projeto
- Decisão pelo Monólito Modular em Django
- Stack completa e justificativas
- Alternativas consideradas e descartadas
- Consequências e trade-offs

### Diagramas
O arquivo [`docs/DIAGRAMAS.md`](docs/DIAGRAMAS.md) contém:
- **Diagrama ER**: Entidades Usuário, Produto, Carrinho, Pedido e seus relacionamentos
- **Diagrama de Fluxo**: Jornada do usuário buscando um produto e adicionando ao carrinho

> Os diagramas estão em sintaxe Mermaid e renderizam automaticamente no GitHub/GitLab.

### Mockup
O arquivo [`index.html`](index.html) é um protótipo funcional da home page com:
- Barra de busca destacada
- Cards de produtos com preço, condição e localização
- Filtros rápidos por categoria
- CTA para anunciar produtos

---

## 🚀 Como visualizar localmente

### Mockup HTML
Basta abrir o arquivo no navegador:
```bash
# Linux / macOS
open index.html

# Windows
start index.html
```

### Diagramas Mermaid
Os diagramas renderizam automaticamente ao abrir os `.md` no GitHub. Para editar/visualizar isoladamente, cole o código em [mermaid.live](https://mermaid.live).

---

## 🗺️ Roadmap

### ✅ Fase 1 — Planejamento (atual)
- [x] Definição da arquitetura (ADR)
- [x] Modelagem ER
- [x] Mockup da home page

### 🔜 Fase 2 — Implementação
- [ ] Setup do projeto Django
- [ ] App `accounts` (cadastro/login)
- [ ] App `catalog` (CRUD de produtos + busca)
- [ ] App `cart` (carrinho de compras)
- [ ] App `orders` (checkout e pedidos)

### 🔮 Fase 3 — Evolução
- [ ] Integração com gateway de pagamento
- [ ] Sistema de avaliações
- [ ] Chat entre comprador e vendedor
- [ ] App mobile

---

## 👥 Equipe

Projeto desenvolvido por **[Nome do Grupo]** como parte do mini-projeto avaliativo.

| Integrante | Função |
|---|---|
| Rafael Monteiro| CEO |
| Gisele| CEO |
| Wagner | CEO |
| Laun | CEO |
| Rafael | CEO |

---

## 📄 Licença

Este projeto é acadêmico e está sob licença MIT.

---

<div align="center">

**Built with ⚡ & caffeine**

</div>
