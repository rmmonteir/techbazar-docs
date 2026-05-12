from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.catalog.models import Product


class Command(BaseCommand):
    help = 'Create sample products for development/demo.'

    def handle(self, *args, **options):
        user_model = get_user_model()
        seller, _ = user_model.objects.get_or_create(
            username='seller_demo',
            defaults={
                'email': 'seller-demo@techbazar.local',
            },
        )

        if not seller.has_usable_password():
            seller.set_password('demo1234')
            seller.save(update_fields=['password'])

        products = [
            {
                'title': 'iPhone 13 Pro 256GB',
                'description': 'Bateria 92% e sem riscos aparentes.',
                'price': Decimal('3450.00'),
                'category': 'Celulares',
                'condition': Product.Condition.SEMI_NEW,
                'stock': 2,
                'is_active': True,
            },
            {
                'title': 'MacBook Air M1 8GB',
                'description': 'Modelo 2020 com caixa original.',
                'price': Decimal('4890.00'),
                'category': 'Notebooks',
                'condition': Product.Condition.USED,
                'stock': 1,
                'is_active': True,
            },
            {
                'title': 'PlayStation 5 Slim',
                'description': 'Inclui 2 controles e 3 jogos.',
                'price': Decimal('3299.00'),
                'category': 'Consoles',
                'condition': Product.Condition.SEMI_NEW,
                'stock': 3,
                'is_active': True,
            },
        ]

        for payload in products:
            Product.objects.get_or_create(
                seller=seller,
                title=payload['title'],
                defaults=payload,
            )

        self.stdout.write(self.style.SUCCESS('Sample products created successfully.'))
