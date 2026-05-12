"""Functional tests for the Cart API (/api/cart/)."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    # Force session creation so _get_or_create_cart works
    client.get("/api/cart/")
    return client


@pytest.fixture
def seller(db):
    return User.objects.create_user(username="cart_seller", password="pass1234")


@pytest.fixture
def active_product(seller, db):
    from apps.catalog.models import Product
    return Product.objects.create(
        seller=seller,
        title="Teclado Mecânico",
        description="Switch Red",
        price="350.00",
        category="Periféricos",
        condition="novo",
        stock=10,
    )


@pytest.fixture
def low_stock_product(seller, db):
    from apps.catalog.models import Product
    return Product.objects.create(
        seller=seller,
        title="Webcam Rara",
        description="Alta demanda",
        price="800.00",
        category="Periféricos",
        condition="usado",
        stock=1,
    )


@pytest.fixture
def inactive_product(seller, db):
    from apps.catalog.models import Product
    return Product.objects.create(
        seller=seller,
        title="Produto Descontinuado",
        description="Fora de linha",
        price="100.00",
        category="Outros",
        condition="usado",
        stock=5,
        is_active=False,
    )


@pytest.mark.django_db
class TestCartGet:
    def test_get_empty_cart_returns_200(self, api_client):
        response = api_client.get("/api/cart/")
        assert response.status_code == 200

    def test_empty_cart_has_zero_totals(self, api_client):
        response = api_client.get("/api/cart/")
        assert response.data["total_items"] == 0
        assert float(response.data["total_amount"]) == 0.0
        assert response.data["items"] == []


@pytest.mark.django_db
class TestCartAddItem:
    def test_add_item_returns_201(self, api_client, active_product):
        response = api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 1}, format="json"
        )
        assert response.status_code == 201

    def test_add_item_updates_total_items(self, api_client, active_product):
        api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 2}, format="json"
        )
        response = api_client.get("/api/cart/")
        assert response.data["total_items"] == 2

    def test_add_item_updates_total_amount(self, api_client, active_product):
        api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 2}, format="json"
        )
        response = api_client.get("/api/cart/")
        assert float(response.data["total_amount"]) == float(active_product.price) * 2

    def test_add_same_item_twice_increments_quantity(self, api_client, active_product):
        api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 1}, format="json"
        )
        api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 2}, format="json"
        )
        response = api_client.get("/api/cart/")
        assert response.data["total_items"] == 3

    def test_add_quantity_exceeding_stock_returns_400(self, api_client, low_stock_product):
        response = api_client.post(
            "/api/cart/items/",
            {"product_id": low_stock_product.pk, "quantity": 99},
            format="json",
        )
        assert response.status_code == 400
        assert "stock" in response.data.get("detail", "").lower()

    def test_add_inactive_product_returns_400(self, api_client, inactive_product):
        response = api_client.post(
            "/api/cart/items/",
            {"product_id": inactive_product.pk, "quantity": 1},
            format="json",
        )
        assert response.status_code == 400

    def test_add_nonexistent_product_returns_404(self, api_client, db):
        response = api_client.post(
            "/api/cart/items/", {"product_id": 99999, "quantity": 1}, format="json"
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestCartUpdateItem:
    def test_patch_quantity_returns_200(self, api_client, active_product):
        add = api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 1}, format="json"
        )
        item_id = add.data["items"][0]["id"]
        response = api_client.patch(
            f"/api/cart/items/{item_id}/", {"quantity": 3}, format="json"
        )
        assert response.status_code == 200
        assert response.data["total_items"] == 3

    def test_patch_quantity_above_stock_returns_400(self, api_client, low_stock_product):
        add = api_client.post(
            "/api/cart/items/",
            {"product_id": low_stock_product.pk, "quantity": 1},
            format="json",
        )
        item_id = add.data["items"][0]["id"]
        response = api_client.patch(
            f"/api/cart/items/{item_id}/", {"quantity": 999}, format="json"
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestCartDeleteItem:
    def test_delete_item_returns_200(self, api_client, active_product):
        add = api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 2}, format="json"
        )
        item_id = add.data["items"][0]["id"]
        response = api_client.delete(f"/api/cart/items/{item_id}/")
        assert response.status_code == 200

    def test_delete_item_empties_cart(self, api_client, active_product):
        add = api_client.post(
            "/api/cart/items/", {"product_id": active_product.pk, "quantity": 1}, format="json"
        )
        item_id = add.data["items"][0]["id"]
        api_client.delete(f"/api/cart/items/{item_id}/")
        response = api_client.get("/api/cart/")
        assert response.data["total_items"] == 0
        assert response.data["items"] == []
