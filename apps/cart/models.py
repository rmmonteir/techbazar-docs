from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.catalog.models import Product


class Cart(models.Model):
	session_key = models.CharField(max_length=64, unique=True)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='carts',
	)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-updated_at',)

	@property
	def total_amount(self):
		total = Decimal('0.00')
		for item in self.items.select_related('product').all():
			total += item.subtotal
		return total

	@property
	def total_items(self):
		return sum(item.quantity for item in self.items.all())

	def __str__(self):
		return f'Cart {self.id} ({self.session_key})'


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='cart_items')
	quantity = models.PositiveIntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product'),
		]
		ordering = ('-created_at',)

	@property
	def subtotal(self):
		return self.product.price * self.quantity

	def clean(self):
		if self.quantity <= 0:
			raise ValidationError({'quantity': 'Quantity must be greater than zero.'})

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.product.title} x{self.quantity}'
