# RISK_ANALYSIS.md — TechBazar: Análise Preditiva de Risco

> **Prompt usado (Passo 4 do exercício):**
> "Atue como Engenheiro de Qualidade. Calcule o fator de risco do código com base na Complexidade Ciclomática e Frequência de Alteração, e informe qual módulo tem maior probabilidade de falhar no próximo deploy."

---

## Escopo da Análise

| Arquivo | Papel no sistema |
|---------|-----------------|
| `cart.py` | Lógica de negócio em memória — `ShoppingCart` e `CartItem` |
| `apps/cart/views.py` | Camada HTTP Django REST — `CartDetailView`, `CartItemAddView`, `CartItemDetailView`, `_get_or_create_cart` |

---

## Metodologia

### Complexidade Ciclomática (CC)

> CC = 1 + número de pontos de decisão (if, elif, for, while, and, or, except)

| Score | Risco |
|-------|-------|
| 1–4 | Baixo |
| 5–7 | Moderado |
| 8–10 | Alto |
| > 10 | Muito alto — refatoração necessária |

### Frequência de Alteração (FA)

Estimativa baseada na volatilidade esperada de cada módulo (escala 1–5):

| Score | Significado |
|-------|-------------|
| 1 | Estável — raramente muda |
| 2 | Pouca mudança esperada |
| 3 | Mudanças moderadas (novos campos, validações) |
| 4 | Ativa — regras de negócio evoluem frequentemente |
| 5 | Muito volátil — múltiplos stakeholders, requisitos em fluxo |

### Score de Risco

```
Risco = CC × FA
```

---

## Análise: `cart.py`

### `CartItem.subtotal` (property)

| Métrica | Valor |
|---------|-------|
| Pontos de decisão | 0 |
| CC | **1** |
| FA | 2 — cálculo simples, muda apenas se a regra de subtotal mudar |
| **Risco** | **2** ✅ |

**Comentário:** Função pura sem branches. Risco mínimo.

---

### `ShoppingCart.add_item`

```python
def add_item(self, name, unit_price, quantity=1):
    if not name or not name.strip():   # +1
        raise ValueError(...)
    if unit_price <= 0:                # +1
        raise ValueError(...)
    if quantity <= 0:                  # +1
        raise ValueError(...)
    existing = self._items.get(name)
    if existing:                       # +1
        existing.quantity += quantity
        ...
        return
    ...
```

| Métrica | Valor |
|---------|-------|
| Pontos de decisão | 4 |
| CC | **5** |
| FA | 4 — novas regras de negócio frequentemente adicionadas aqui (ex.: limites de quantity, categorias restritas) |
| **Risco** | **20** 🔴 |

**Comentário:** Método mais complexo do módulo. Qualquer nova regra de validação aumenta o risco sem cobertura de teste proporcional.

---

### `ShoppingCart.discount_amount`

```python
def discount_amount(self, threshold=200.0, rate=0.1):
    if threshold < 0:              # +1
        raise ValueError(...)
    if rate < 0 or rate > 1:       # +2 (operador 'or')
        raise ValueError(...)
    current_subtotal = self.subtotal()
    if current_subtotal >= threshold:  # +1
        return current_subtotal * rate
    return 0.0
```

| Métrica | Valor |
|---------|-------|
| Pontos de decisão | 4 (incluindo `or`) |
| CC | **5** |
| FA | 5 — regras de desconto mudam com campanhas, cupons, perfil de usuário |
| **Risco** | **25** 🔴🔴 |

**Comentário:** Maior score de risco do projeto. Regras de desconto são inerentemente voláteis e qualquer alteração nos parâmetros `threshold`/`rate` pode quebrar integrações silenciosamente.

---

### `ShoppingCart.remove_item`

| Métrica | Valor |
|---------|-------|
| CC | **2** |
| FA | 2 |
| **Risco** | **4** ✅ |

---

### `ShoppingCart.total`

| Métrica | Valor |
|---------|-------|
| CC | **1** (delega para `subtotal` e `discount_amount`) |
| FA | 3 — exposto como interface pública, pode receber novos parâmetros |
| **Risco** | **3** ✅ |

---

## Análise: `apps/cart/views.py`

### `_get_or_create_cart`

```python
def _get_or_create_cart(request):
    if not request.session.session_key:                              # +1
        request.session.create()
    ...
    if request.user.is_authenticated and cart.user_id is None:      # +2 (and)
        cart.user = request.user
        cart.save(...)
    return cart
```

| Métrica | Valor |
|---------|-------|
| Pontos de decisão | 3 |
| CC | **4** |
| FA | 3 — muda quando autenticação evolui (JWT, OAuth, multi-device) |
| **Risco** | **12** 🟡 |

**Comentário:** Função auxiliar compartilhada por todas as views do carrinho. Um bug aqui afeta toda a feature de cart.

---

### `CartItemAddView.post`

```python
def post(self, request):
    ...
    if not product.is_active:              # +1
        return Response(400)
    cart_item, created = CartItem.objects.get_or_create(...)
    if not created:                        # +1
        cart_item.quantity += data['quantity']
    if cart_item.quantity > product.stock: # +1
        return Response(400)
    ...
```

| Métrica | Valor |
|---------|-------|
| Pontos de decisão | 3 |
| CC | **4** |
| FA | 4 — ponto central de negócio: validações de estoque, promoções, limites por usuário |
| **Risco** | **16** 🔴 |

**Comentário:** View mais complexa da camada HTTP. Mistura orquestração de sessão, validação de domínio e persistência — candidata a extração de lógica para uma camada de serviço.

---

### `CartItemDetailView.patch`

```python
def patch(self, request, item_id):
    ...
    if quantity > item.product.stock:  # +1
        return Response(400)
    ...
```

| Métrica | Valor |
|---------|-------|
| CC | **2** |
| FA | 3 |
| **Risco** | **6** ✅ |

---

### `CartItemDetailView.delete` e `CartDetailView.get`

| Método | CC | FA | Risco |
|--------|----|----|-------|
| `delete` | 1 | 2 | **2** ✅ |
| `get` | 1 | 1 | **1** ✅ |

---

## Tabela Consolidada de Riscos

| Módulo | Função | CC | FA | Risco | Status |
|--------|--------|----|----|-------|--------|
| `cart.py` | `discount_amount` | 5 | 5 | **25** | 🔴🔴 CRÍTICO |
| `cart.py` | `add_item` | 5 | 4 | **20** | 🔴 ALTO |
| `apps/cart/views.py` | `CartItemAddView.post` | 4 | 4 | **16** | 🔴 ALTO |
| `apps/cart/views.py` | `_get_or_create_cart` | 4 | 3 | **12** | 🟡 MODERADO |
| `apps/cart/views.py` | `CartItemDetailView.patch` | 2 | 3 | **6** | ✅ BAIXO |
| `cart.py` | `remove_item` | 2 | 2 | **4** | ✅ BAIXO |
| `cart.py` | `total` | 1 | 3 | **3** | ✅ BAIXO |
| `cart.py` | `subtotal` (property) | 1 | 2 | **2** | ✅ BAIXO |
| `apps/cart/views.py` | `CartItemDetailView.delete` | 1 | 2 | **2** | ✅ BAIXO |
| `apps/cart/views.py` | `CartDetailView.get` | 1 | 1 | **1** | ✅ BAIXO |

---

## Diagnóstico Preditivo

### Módulo com maior probabilidade de falhar no próximo deploy

> **`ShoppingCart.discount_amount` em `cart.py`** — Score 25 (CRÍTICO)

**Razão:** Combina CC=5 com FA=5. Regras de desconto estão diretamente atreladas a decisões de negócio (campanhas, cupons, fidelidade) e tendem a mudar frequentemente sem que os testes unitários existentes sejam atualizados na mesma cadência. Qualquer modificação nos parâmetros `threshold` e `rate` pode introduzir regressões silenciosas que só aparecem em produção.

**Segundo maior risco:** `ShoppingCart.add_item` — Score 20. Cada nova validação de produto (ex.: limite por CPF, restrição de categoria) adiciona branches que requerem cobertura de teste dedicada.

---

## Recomendações

| Prioridade | Ação |
|-----------|------|
| 🔴 Imediata | Aumentar cobertura de `discount_amount` com testes parametrizados para todos os limites de `threshold` e `rate` |
| 🔴 Curto prazo | Extrair regras de negócio de `CartItemAddView.post` para uma camada de serviço (`CartService`) — reduz CC da view e facilita mock nos testes |
| 🟡 Médio prazo | Adicionar testes de mutação (`mutmut`) em `cart.py` para detectar lógica condicional frágil |
| ✅ Monitorar | `_get_or_create_cart` — inofensivo agora, mas crítico quando autenticação evoluir para JWT/OAuth |

---

*Gerado em: 2026-05-15 | Ferramenta: GitHub Copilot (Claude Sonnet 4.6) | Exercício Hands-on 3*
