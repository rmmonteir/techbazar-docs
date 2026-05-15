"""
Testes E2E — TechBazar frontend (/app/)
Exercício Hands-on 3: E2E com Playwright Python (pytest-playwright)

Pré-requisitos:
  - Servidor Django rodando em http://localhost:8000
  - playwright install chromium

Execução:
  pytest tests/test_e2e.py --headed          # com browser visível
  pytest tests/test_e2e.py                   # headless (padrão)

Regras de seletor (anti-flaky):
  - SEMPRE usar data-testid ou seletores por texto
  - NUNCA usar seletores CSS baseados em classes utilitárias (Tailwind)
"""

import re

import pytest
from playwright.sync_api import APIRequestContext, Page, Playwright, expect

BASE_URL = "http://localhost:8000"


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def ensure_products(playwright: Playwright):
    """
    Garante que ao menos um produto ativo existe no banco antes dos testes E2E.
    Cria via API se a listagem estiver vazia.
    """
    ctx: APIRequestContext = playwright.request.new_context(base_url=BASE_URL)
    try:
        response = ctx.get("/api/products/")
        data = response.json()
        results = data.get("results", []) if isinstance(data, dict) else data
        if not results:
            ctx.post(
                "/api/products/",
                data={
                    "title": "Produto E2E Test",
                    "description": "Produto criado automaticamente para testes E2E.",
                    "price": "299.99",
                    "category": "Periféricos",
                    "condition": "novo",
                    "stock": 10,
                },
            )
    finally:
        ctx.dispose()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _parse_cart_count(text: str) -> int:
    """Extrai o número do formato '[N]' exibido no header do carrinho."""
    match = re.search(r"\d+", text)
    assert match, f"Não foi possível extrair número do contador: {text!r}"
    return int(match.group())


# ─── Testes: carregamento da página ──────────────────────────────────────────

class TestPageLoad:
    def test_page_loads_with_title(self, page: Page):
        """Página /app/ deve carregar e exibir 'TechBazar' no título."""
        page.goto(f"{BASE_URL}/app/")
        expect(page).to_have_title(re.compile(r"TechBazar", re.IGNORECASE))

    def test_header_brand_visible(self, page: Page):
        """Logo 'TechBazar' deve estar visível no header."""
        page.goto(f"{BASE_URL}/app/")
        brand = page.get_by_text("TechBazar", exact=False).first
        expect(brand).to_be_visible()

    def test_cart_counter_visible(self, page: Page):
        """Contador do carrinho [N] deve estar visível no header."""
        page.goto(f"{BASE_URL}/app/")
        counter = page.locator('[data-testid="cart-count"]')
        expect(counter).to_be_visible()

    def test_search_input_visible(self, page: Page):
        """Campo de busca deve estar visível e aceitável."""
        page.goto(f"{BASE_URL}/app/")
        search = page.locator('[data-testid="search-input"]')
        expect(search).to_be_visible()
        expect(search).to_be_editable()


# ─── Testes: grid de produtos ─────────────────────────────────────────────────

class TestProductGrid:
    def test_product_cards_render(self, page: Page, ensure_products):
        """Grid deve exibir ao menos um card de produto após resposta da API."""
        page.goto(f"{BASE_URL}/app/")
        first_card = page.locator('[data-testid="product-card"]').first
        expect(first_card).to_be_visible(timeout=10_000)

    def test_each_card_has_add_button(self, page: Page, ensure_products):
        """Cada card visível deve ter um botão de adicionar ao carrinho."""
        page.goto(f"{BASE_URL}/app/")
        page.locator('[data-testid="product-card"]').first.wait_for(timeout=10_000)
        first_btn = page.locator('[data-testid="add-to-cart-btn"]').first
        expect(first_btn).to_be_visible()
        expect(first_btn).to_be_enabled()


# ─── Testes: adicionar ao carrinho ───────────────────────────────────────────

class TestAddToCart:
    def test_cart_counter_increments_on_add(self, page: Page, ensure_products):
        """
        Clicar em 'adicionar ao carrinho' deve incrementar o contador no header.

        Fluxo:
          1. Abre /app/
          2. Aguarda produtos carregarem
          3. Lê contador inicial [N]
          4. Clica no primeiro botão '+'
          5. Aguarda contador mudar
          6. Verifica que o novo valor é N+1
        """
        page.goto(f"{BASE_URL}/app/")
        page.locator('[data-testid="product-card"]').first.wait_for(timeout=10_000)

        counter = page.locator('[data-testid="cart-count"]')
        initial_count = _parse_cart_count(counter.inner_text())

        page.locator('[data-testid="add-to-cart-btn"]').first.click()

        # Aguarda o texto do contador mudar (a API responde e o JS atualiza)
        expect(counter).not_to_have_text(f"[{initial_count}]", timeout=5_000)

        updated_count = _parse_cart_count(counter.inner_text())
        assert updated_count == initial_count + 1, (
            f"Esperava contador {initial_count + 1}, obteve {updated_count}"
        )

    def test_add_product_twice_accumulates_quantity(self, page: Page, ensure_products):
        """
        Adicionar o mesmo produto duas vezes deve acumular quantity no carrinho
        (a API incrementa, não cria dois itens) e o contador deve refletir.
        """
        page.goto(f"{BASE_URL}/app/")
        page.locator('[data-testid="product-card"]').first.wait_for(timeout=10_000)

        counter = page.locator('[data-testid="cart-count"]')
        initial_count = _parse_cart_count(counter.inner_text())

        first_btn = page.locator('[data-testid="add-to-cart-btn"]').first

        # Primeiro clique
        first_btn.click()
        expect(counter).not_to_have_text(f"[{initial_count}]", timeout=5_000)
        after_first = _parse_cart_count(counter.inner_text())

        # Aguarda o botão ser re-habilitado (cooldown de 1s no JS)
        expect(first_btn).to_be_enabled(timeout=3_000)

        # Segundo clique
        first_btn.click()
        expect(counter).not_to_have_text(f"[{after_first}]", timeout=5_000)
        after_second = _parse_cart_count(counter.inner_text())

        assert after_second == initial_count + 2, (
            f"Esperava contador {initial_count + 2} após dois cliques, obteve {after_second}"
        )


# ─── Testes: busca ───────────────────────────────────────────────────────────

class TestSearch:
    def test_search_with_no_results_clears_grid(self, page: Page, ensure_products):
        """
        Busca por texto inexistente deve limpar o grid de produtos
        (nenhum data-testid='product-card' visível).
        """
        page.goto(f"{BASE_URL}/app/")
        page.locator('[data-testid="product-card"]').first.wait_for(timeout=10_000)

        search = page.locator('[data-testid="search-input"]')
        search.fill("xyzabcdef_inexistente_99999")

        # Debounce de 300ms + tempo de resposta da API
        page.wait_for_timeout(800)

        cards = page.locator('[data-testid="product-card"]')
        assert cards.count() == 0, (
            f"Grid deveria estar vazio para busca sem resultados, mas encontrou {cards.count()} cards"
        )

    def test_clearing_search_restores_grid(self, page: Page, ensure_products):
        """
        Limpar o campo de busca deve restaurar a listagem completa de produtos.
        """
        page.goto(f"{BASE_URL}/app/")
        page.locator('[data-testid="product-card"]').first.wait_for(timeout=10_000)

        search = page.locator('[data-testid="search-input"]')

        # Filtra sem resultados
        search.fill("xyzabcdef_inexistente_99999")
        page.wait_for_timeout(800)

        # Limpa a busca
        search.fill("")
        page.wait_for_timeout(800)

        # Produtos devem reaparecer
        expect(page.locator('[data-testid="product-card"]').first).to_be_visible(timeout=5_000)
