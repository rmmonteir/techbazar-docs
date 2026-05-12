# Diretrizes de IA para Testes

Este arquivo define um formato minimo para gerar testes de forma consistente no projeto.

## Regras

1. Leia a implementacao alvo antes de escrever testes.
2. Estruture os testes no padrao AAA:
- Arrange: preparar entradas e estado inicial.
- Act: executar a acao testada.
- Assert: validar o resultado esperado.
3. Cubra caminhos felizes e casos de borda.
4. Prefira testes unitarios deterministas e independentes.
5. Nomeie os testes de forma descritiva.

## Requisitos para o exercicio de carrinho

- Arquivo de implementacao: `cart.py`
- Arquivo de testes: `tests/test_cart.py`
- Classe alvo: `ShoppingCart`
- Cobertura minima no CI: 80%
- Runner no CI: `uv run pytest`
