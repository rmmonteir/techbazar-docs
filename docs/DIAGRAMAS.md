# DIAGRAMAS - TechBazar

Este documento contém os diagramas conceituais do sistema TechBazar em sintaxe **Mermaid**.

> Para visualizar: cole o código em [https://mermaid.live](https://mermaid.live) ou abra este `.md` no GitHub/GitLab (renderização automática).

---

## 1. Diagrama Entidade-Relacionamento (ER)

Representa as principais entidades do domínio e seus relacionamentos.

```mermaid
erDiagram
    USUARIO ||--o{ PRODUTO : "anuncia"
    USUARIO ||--o{ PEDIDO : "realiza"
    PRODUTO ||--o{ ITEM_PEDIDO : "compõe"
    PEDIDO ||--|{ ITEM_PEDIDO : "contém"
    USUARIO ||--o| CARRINHO : "possui"
    CARRINHO ||--o{ ITEM_CARRINHO : "contém"
    PRODUTO ||--o{ ITEM_CARRINHO : "está_em"

    USUARIO {
        int id PK
        string nome
        string email UK
        string senha_hash
        string telefone
        string cpf
        datetime criado_em
    }

    PRODUTO {
        int id PK
        int vendedor_id FK
        string titulo
        text descricao
        decimal preco
        string categoria
        string condicao
        string imagem_url
        int estoque
        boolean ativo
        datetime criado_em
    }

    CARRINHO {
        int id PK
        int usuario_id FK
        datetime atualizado_em
    }

    ITEM_CARRINHO {
        int id PK
        int carrinho_id FK
        int produto_id FK
        int quantidade
    }

    PEDIDO {
        int id PK
        int comprador_id FK
        decimal total
        string status
        string endereco_entrega
        string forma_pagamento
        datetime criado_em
    }

    ITEM_PEDIDO {
        int id PK
        int pedido_id FK
        int produto_id FK
        int quantidade
        decimal preco_unitario
    }
```

### Notas sobre o modelo

- **USUARIO** pode ser tanto comprador quanto vendedor (papel definido pelo contexto da operação).
- **PRODUTO** pertence sempre a um vendedor (`vendedor_id`).
- **CARRINHO** é único por usuário (relação 1-1 opcional).
- **PEDIDO** congela o `preco_unitario` no momento da compra (snapshot histórico).
- Status do pedido: `pendente | pago | enviado | entregue | cancelado`.

---

## 2. Diagrama de Fluxo: Buscar Produto e Adicionar ao Carrinho

Representa a jornada do usuário desde a busca até a confirmação do item no carrinho.

```mermaid
flowchart TD
    A([Usuário acessa Home]) --> B[Digita termo na barra de busca]
    B --> C[Sistema consulta catálogo]
    C --> D{Produtos encontrados?}

    D -->|Não| E[Exibe mensagem: nenhum resultado]
    E --> B

    D -->|Sim| F[Exibe lista de produtos]
    F --> G[Usuário clica em um produto]
    G --> H[Exibe página de detalhes]
    H --> I{Usuário deseja comprar?}

    I -->|Não| F
    I -->|Sim| J[Clica em 'Adicionar ao Carrinho']

    J --> K{Usuário está logado?}
    K -->|Não| L[Redireciona para Login/Cadastro]
    L --> M[Usuário autentica]
    M --> N[Adiciona produto ao carrinho]

    K -->|Sim| N

    N --> O[Sistema valida estoque]
    O --> P{Estoque disponível?}

    P -->|Não| Q[Mostra erro: produto indisponível]
    Q --> H

    P -->|Sim| R[Persiste item no carrinho]
    R --> S[Exibe confirmação + badge atualizado]
    S --> T([Fluxo concluído])
```

### Pontos-chave do fluxo

1. **Busca pública**: não exige login para pesquisar ou visualizar produtos.
2. **Login obrigatório no carrinho**: o usuário só pode adicionar itens após autenticar.
3. **Validação de estoque**: feita server-side antes de persistir.
4. **Feedback visual**: badge do carrinho é atualizado em tempo real (HTMX ou JS).

---

## 3. Próximos diagramas (futuros)

- Fluxo de checkout e pagamento
- Diagrama de sequência da API REST
- Diagrama de componentes (camadas Django)
