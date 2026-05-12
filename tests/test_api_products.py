"""Functional tests for the Products API (/api/products/)."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def seller(db):
    return User.objects.create_user(username="seller_test", password="pass1234")


@pytest.fixture
def product_payload(seller):
    return {
        "seller": seller.pk,
        "title": "Notebook Gamer",
        "description": "RTX 4060, 16GB RAM",
        "price": "4500.00",
        "category": "Notebooks",
        "condition": "novo",
        "stock": 5,
    }


@pytest.fixture
def product(api_client, product_payload, db):
    response = api_client.post("/api/products/", product_payload, format="json")
    assert response.status_code == 201
    return response.data


@pytest.mark.django_db
class TestProductList:
    def test_list_returns_200(self, api_client):
        response = api_client.get("/api/products/")
        assert response.status_code == 200

    def test_list_is_paginated(self, api_client):
        response = api_client.get("/api/products/")
        assert "results" in response.data
        assert "count" in response.data

    def test_search_by_title(self, api_client, product):
        response = api_client.get("/api/products/?search=Notebook")
        assert response.status_code == 200
        titles = [p["title"] for p in response.data["results"]]
        assert any("Notebook" in t for t in titles)

    def test_search_no_match_returns_empty(self, api_client, product):
        response = api_client.get("/api/products/?search=xyzinexistente")
        assert response.status_code == 200
        assert response.data["count"] == 0

    def test_ordering_by_price(self, api_client, seller, db):
        api_client.post("/api/products/", {**{"seller": seller.pk, "title": "A", "description": "d",
            "price": "100.00", "category": "Cat", "condition": "novo", "stock": 1}}, format="json")
        api_client.post("/api/products/", {**{"seller": seller.pk, "title": "B", "description": "d",
            "price": "50.00", "category": "Cat", "condition": "novo", "stock": 1}}, format="json")
        response = api_client.get("/api/products/?ordering=price")
        assert response.status_code == 200
        prices = [float(p["price"]) for p in response.data["results"]]
        assert prices == sorted(prices)


@pytest.mark.django_db
class TestProductCreate:
    def test_create_returns_201(self, api_client, product_payload):
        response = api_client.post("/api/products/", product_payload, format="json")
        assert response.status_code == 201

    def test_create_returns_correct_fields(self, api_client, product_payload):
        response = api_client.post("/api/products/", product_payload, format="json")
        assert response.data["title"] == product_payload["title"]
        assert response.data["category"] == product_payload["category"]
        assert float(response.data["price"]) == float(product_payload["price"])

    def test_create_with_negative_price_returns_400(self, api_client, product_payload):
        product_payload["price"] = "-10.00"
        response = api_client.post("/api/products/", product_payload, format="json")
        assert response.status_code == 400

    def test_create_missing_required_field_returns_400(self, api_client, product_payload):
        del product_payload["title"]
        response = api_client.post("/api/products/", product_payload, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestProductDetail:
    def test_retrieve_returns_200(self, api_client, product):
        response = api_client.get(f"/api/products/{product['id']}/")
        assert response.status_code == 200
        assert response.data["id"] == product["id"]

    def test_retrieve_nonexistent_returns_404(self, api_client, db):
        response = api_client.get("/api/products/99999/")
        assert response.status_code == 404

    def test_full_update_returns_200(self, api_client, product, seller):
        payload = {
            "seller": seller.pk,
            "title": "Notebook Gamer Atualizado",
            "description": "Nova descricao",
            "price": "5000.00",
            "category": "Notebooks",
            "condition": "seminovo",
            "stock": 3,
        }
        response = api_client.put(f"/api/products/{product['id']}/", payload, format="json")
        assert response.status_code == 200
        assert response.data["title"] == "Notebook Gamer Atualizado"

    def test_partial_update_price(self, api_client, product):
        response = api_client.patch(
            f"/api/products/{product['id']}/", {"price": "3999.00"}, format="json"
        )
        assert response.status_code == 200
        assert float(response.data["price"]) == 3999.00

    def test_delete_returns_204(self, api_client, product):
        response = api_client.delete(f"/api/products/{product['id']}/")
        assert response.status_code == 204

    def test_delete_then_retrieve_returns_404(self, api_client, product):
        api_client.delete(f"/api/products/{product['id']}/")
        response = api_client.get(f"/api/products/{product['id']}/")
        assert response.status_code == 404
