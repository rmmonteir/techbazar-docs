erDiagram
    USUARIO ||--o{ PRODUTO : "anuncia"
    USUARIO ||--o{ PEDIDO : "realiza"
    PRODUTO ||--o{ ITEM_PEDIDO : "compoe"
    PEDIDO ||--|{ ITEM_PEDIDO : "contem"
    USUARIO ||--o| CARRINHO : "possui"
    CARRINHO ||--o{ ITEM_CARRINHO : "contem"
    PRODUTO ||--o{ ITEM_CARRINHO : "esta_em"

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

    