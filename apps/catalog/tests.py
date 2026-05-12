from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Product


class ProductModelTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='seller_model',
			email='seller-model@test.local',
		)

	def test_invalid_price_raises_validation_error(self):
		product = Product(
			seller=self.user,
			title='Produto Invalido',
			description='Teste',
			price='0.00',
			category='Categoria',
			condition=Product.Condition.USED,
			stock=1,
			is_active=True,
		)

		with self.assertRaises(ValidationError):
			product.full_clean()

	def test_valid_product_is_saved(self):
		product = Product.objects.create(
			seller=self.user,
			title='Produto Valido',
			description='Teste',
			price='120.00',
			category='Categoria',
			condition=Product.Condition.USED,
			stock=2,
			is_active=True,
		)

		self.assertIsNotNone(product.id)
