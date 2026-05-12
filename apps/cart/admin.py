from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ('id', 'session_key', 'user', 'updated_at')
	search_fields = ('session_key', 'user__username', 'user__email')
	ordering = ('-updated_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'cart', 'product', 'quantity', 'created_at')
	search_fields = ('product__title', 'cart__session_key')
	ordering = ('-created_at',)

# Register your models here.
