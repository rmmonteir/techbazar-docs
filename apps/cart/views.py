from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import Product

from .models import Cart, CartItem
from .serializers import (
	CartItemAddSerializer,
	CartItemUpdateSerializer,
	CartSerializer,
)


def _get_or_create_cart(request):
	if not request.session.session_key:
		request.session.create()

	session_key = request.session.session_key
	cart, _ = Cart.objects.get_or_create(session_key=session_key)

	if request.user.is_authenticated and cart.user_id is None:
		cart.user = request.user
		cart.save(update_fields=['user', 'updated_at'])

	return cart


class CartDetailView(APIView):
	def get(self, request):
		cart = _get_or_create_cart(request)
		serializer = CartSerializer(cart)
		return Response(serializer.data)


class CartItemAddView(APIView):
	def post(self, request):
		payload = CartItemAddSerializer(data=request.data)
		payload.is_valid(raise_exception=True)
		data = payload.validated_data

		cart = _get_or_create_cart(request)
		product = get_object_or_404(Product, pk=data['product_id'])

		if not product.is_active:
			return Response(
				{'detail': 'Product is inactive.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		cart_item, created = CartItem.objects.get_or_create(
			cart=cart,
			product=product,
			defaults={'quantity': data['quantity']},
		)

		if not created:
			cart_item.quantity += data['quantity']

		if cart_item.quantity > product.stock:
			return Response(
				{'detail': 'Quantity exceeds available stock.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		cart_item.save()
		cart.save(update_fields=['updated_at'])

		return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
	def patch(self, request, item_id):
		payload = CartItemUpdateSerializer(data=request.data)
		payload.is_valid(raise_exception=True)
		quantity = payload.validated_data['quantity']

		cart = _get_or_create_cart(request)
		item = get_object_or_404(CartItem, pk=item_id, cart=cart)

		if quantity > item.product.stock:
			return Response(
				{'detail': 'Quantity exceeds available stock.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		item.quantity = quantity
		item.save()
		cart.save(update_fields=['updated_at'])

		return Response(CartSerializer(cart).data)

	def delete(self, request, item_id):
		cart = _get_or_create_cart(request)
		item = get_object_or_404(CartItem, pk=item_id, cart=cart)
		item.delete()
		cart.save(update_fields=['updated_at'])

		return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
