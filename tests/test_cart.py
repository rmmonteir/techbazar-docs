import pytest

from cart import ShoppingCart


class TestShoppingCart:
    def test_add_item_updates_subtotal_and_total_items(self):
        # Arrange
        cart = ShoppingCart()

        # Act
        cart.add_item(name="Mouse", unit_price=100.0, quantity=2)

        # Assert
        assert cart.total_items() == 2
        assert cart.subtotal() == 200.0

    def test_add_same_item_twice_accumulates_quantity(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="Teclado", unit_price=80.0, quantity=1)

        # Act
        cart.add_item(name="Teclado", unit_price=80.0, quantity=2)

        # Assert
        assert cart.total_items() == 3
        assert cart.subtotal() == 240.0

    def test_empty_cart_has_zero_values(self):
        # Arrange
        cart = ShoppingCart()

        # Act
        subtotal = cart.subtotal()
        total = cart.total()
        total_items = cart.total_items()

        # Assert
        assert cart.is_empty() is True
        assert subtotal == 0.0
        assert total == 0.0
        assert total_items == 0

    def test_exact_threshold_applies_discount(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="Headset", unit_price=200.0, quantity=1)

        # Act
        discount = cart.discount_amount(threshold=200.0, rate=0.1)
        total = cart.total(threshold=200.0, rate=0.1)

        # Assert
        assert discount == 20.0
        assert total == 180.0

    def test_below_threshold_does_not_apply_discount(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="Webcam", unit_price=199.99, quantity=1)

        # Act
        discount = cart.discount_amount(threshold=200.0, rate=0.1)

        # Assert
        assert discount == 0.0

    def test_add_item_with_invalid_quantity_raises(self):
        # Arrange
        cart = ShoppingCart()

        # Act / Assert
        with pytest.raises(ValueError, match="Quantity must be greater than zero"):
            cart.add_item(name="Monitor", unit_price=999.0, quantity=0)

    def test_remove_nonexistent_item_raises(self):
        # Arrange
        cart = ShoppingCart()

        # Act / Assert
        with pytest.raises(KeyError):
            cart.remove_item("Nao existe")

    def test_remove_existing_item_empties_cart(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="SSD", unit_price=300.0, quantity=1)

        # Act
        cart.remove_item("SSD")

        # Assert
        assert cart.is_empty() is True

    def test_clear_removes_all_items(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="GPU", unit_price=1500.0, quantity=1)
        cart.add_item(name="CPU", unit_price=800.0, quantity=2)

        # Act
        cart.clear()

        # Assert
        assert cart.is_empty() is True
        assert cart.total_items() == 0

    def test_items_property_returns_copy(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="RAM", unit_price=250.0, quantity=4)

        # Act
        snapshot = cart.items

        # Assert
        assert "RAM" in snapshot
        assert snapshot["RAM"].quantity == 4

    def test_add_item_with_empty_name_raises(self):
        # Arrange
        cart = ShoppingCart()

        # Act / Assert
        with pytest.raises(ValueError, match="Item name cannot be empty"):
            cart.add_item(name="   ", unit_price=50.0, quantity=1)

    def test_add_item_with_zero_price_raises(self):
        # Arrange
        cart = ShoppingCart()

        # Act / Assert
        with pytest.raises(ValueError, match="Unit price must be greater than zero"):
            cart.add_item(name="Pendrive", unit_price=0.0, quantity=1)

    def test_discount_with_negative_threshold_raises(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="Cabo", unit_price=50.0, quantity=1)

        # Act / Assert
        with pytest.raises(ValueError, match="Threshold cannot be negative"):
            cart.discount_amount(threshold=-1.0)

    def test_discount_with_invalid_rate_raises(self):
        # Arrange
        cart = ShoppingCart()
        cart.add_item(name="Cabo", unit_price=50.0, quantity=1)

        # Act / Assert
        with pytest.raises(ValueError, match="Rate must be between 0 and 1"):
            cart.discount_amount(rate=1.5)
