from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Product
        fields = (
            'id',
            'seller',
            'title',
            'description',
            'price',
            'category',
            'condition',
            'image_url',
            'stock',
            'is_active',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative.')
        return value

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        request = self.context.get('request')

        if instance and request and request.method in ('PUT', 'PATCH') and not instance.is_active:
            raise serializers.ValidationError(
                'Inactive products cannot be changed. Activate it first.'
            )

        return attrs
