from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.catalog.models import Product


class CartApiTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='seller_test',
			email='seller@test.local',
		)
		self.product = Product.objects.create(
			seller=self.user,
			title='Produto Teste',
			description='Descricao de teste',
			price='100.00',
			category='Acessorios',
			condition=Product.Condition.USED,
			stock=5,
			is_active=True,
		)

	def test_add_item_and_get_cart(self):
		add_response = self.client.post(
			'/api/cart/items/',
			{'product_id': self.product.id, 'quantity': 2},
			content_type='application/json',
		)

		self.assertEqual(add_response.status_code, 201)
		self.assertEqual(add_response.json()['total_items'], 2)

		detail_response = self.client.get('/api/cart/')
		self.assertEqual(detail_response.status_code, 200)
		payload = detail_response.json()
		self.assertEqual(payload['total_items'], 2)
		self.assertEqual(len(payload['items']), 1)

	def test_add_same_item_twice_increments_quantity(self):
		self.client.post(
			'/api/cart/items/',
			{'product_id': self.product.id, 'quantity': 1},
			content_type='application/json',
		)
		second_response = self.client.post(
			'/api/cart/items/',
			{'product_id': self.product.id, 'quantity': 2},
			content_type='application/json',
		)

		self.assertEqual(second_response.status_code, 201)
		payload = second_response.json()
		self.assertEqual(payload['total_items'], 3)
		self.assertEqual(payload['items'][0]['quantity'], 3)

	def test_add_item_over_stock_returns_bad_request(self):
		response = self.client.post(
			'/api/cart/items/',
			{'product_id': self.product.id, 'quantity': 99},
			content_type='application/json',
		)
		self.assertEqual(response.status_code, 400)

	def test_update_and_remove_item(self):
		add_response = self.client.post(
			'/api/cart/items/',
			{'product_id': self.product.id, 'quantity': 1},
			content_type='application/json',
		)
		item_id = add_response.json()['items'][0]['id']

		update_response = self.client.patch(
			f'/api/cart/items/{item_id}/',
			{'quantity': 4},
			content_type='application/json',
		)
		self.assertEqual(update_response.status_code, 200)
		self.assertEqual(update_response.json()['items'][0]['quantity'], 4)

		delete_response = self.client.delete(f'/api/cart/items/{item_id}/')
		self.assertEqual(delete_response.status_code, 200)
		self.assertEqual(delete_response.json()['total_items'], 0)
		self.assertEqual(len(delete_response.json()['items']), 0)
