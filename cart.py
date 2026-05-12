from dataclasses import dataclass


@dataclass
class CartItem:
    name: str
    unit_price: float
    quantity: int

    @property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity


class ShoppingCart:
    def __init__(self) -> None:
        self._items: dict[str, CartItem] = {}

    @property
    def items(self) -> dict[str, CartItem]:
        return dict(self._items)

    def add_item(self, name: str, unit_price: float, quantity: int = 1) -> None:
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty.")
        if unit_price <= 0:
            raise ValueError("Unit price must be greater than zero.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        existing = self._items.get(name)
        if existing:
            existing.quantity += quantity
            existing.unit_price = unit_price
            return

        self._items[name] = CartItem(name=name, unit_price=unit_price, quantity=quantity)

    def remove_item(self, name: str) -> None:
        if name not in self._items:
            raise KeyError(f"Item '{name}' not found in cart.")
        del self._items[name]

    def clear(self) -> None:
        self._items.clear()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def total_items(self) -> int:
        return sum(item.quantity for item in self._items.values())

    def subtotal(self) -> float:
        return sum(item.subtotal for item in self._items.values())

    def discount_amount(self, threshold: float = 200.0, rate: float = 0.1) -> float:
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if rate < 0 or rate > 1:
            raise ValueError("Rate must be between 0 and 1.")

        current_subtotal = self.subtotal()
        if current_subtotal >= threshold:
            return current_subtotal * rate
        return 0.0

    def total(self, threshold: float = 200.0, rate: float = 0.1) -> float:
        return self.subtotal() - self.discount_amount(threshold=threshold, rate=rate)
