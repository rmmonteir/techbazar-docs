from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'category', 'price', 'stock', 'is_active', 'created_at')
	list_filter = ('is_active', 'category', 'condition', 'created_at')
	search_fields = ('title', 'description', 'category')
	ordering = ('-created_at',)

# Register your models here.
