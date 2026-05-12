from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.select_related('seller').all()
	serializer_class = ProductSerializer
	search_fields = ('title', 'category')
	ordering_fields = ('price', 'created_at', 'title')
	ordering = ('-created_at',)
