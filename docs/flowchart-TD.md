flowchart TD
    A([Usuario acessa Home]) --> B[Digita termo na barra de busca]
    B --> C[Sistema consulta catalogo]
    C --> D{Produtos encontrados?}

    D -->|Nao| E[Exibe mensagem: nenhum resultado]
    E --> B

    D -->|Sim| F[Exibe lista de produtos]
    F --> G[Usuario clica em um produto]
    G --> H[Exibe pagina de detalhes]
    H --> I{Usuario deseja comprar?}

    I -->|Nao| F
    I -->|Sim| J[Clica em Adicionar ao Carrinho]

    J --> K{Usuario esta logado?}
    K -->|Nao| L[Redireciona para Login/Cadastro]
    L --> M[Usuario autentica]
    M --> N[Adiciona produto ao carrinho]

    K -->|Sim| N

    N --> O[Sistema valida estoque]
    O --> P{Estoque disponivel?}

    P -->|Nao| Q[Mostra erro: produto indisponivel]
    Q --> H

    P -->|Sim| R[Persiste item no carrinho]
    R --> S[Exibe confirmacao + badge atualizado]
    S --> T([Fluxo concluido])