from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
	class Condition(models.TextChoices):
		NEW = 'novo', 'Novo'
		USED = 'usado', 'Usado'
		SEMI_NEW = 'seminovo', 'Seminovo'

	seller = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name='products',
	)
	title = models.CharField(max_length=150)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.CharField(max_length=80)
	condition = models.CharField(
		max_length=20,
		choices=Condition.choices,
		default=Condition.USED,
	)
	image_url = models.URLField(blank=True)
	stock = models.PositiveIntegerField(default=1)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at',)

	def clean(self):
		if self.price is not None and self.price <= Decimal('0'):
			raise ValidationError({'price': 'Price must be greater than zero.'})
		if self.stock < 0:
			raise ValidationError({'stock': 'Stock cannot be negative.'})

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.title} ({self.category})'
