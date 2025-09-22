from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add product to the database"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category1, _ = Category.objects.get_or_create(
            name="Телефоны",
            description="Стильный внешний вид, ёмкий аккумулятор, большая оперативная память и производительный процессор",
        )

        products1 = [
            {
                "name": "Samsung",
                "description": "RAM 12 ГБ, память 456 ГБ",
                "category": category1,
                "image": "",
                "price": 40000,
            },
            {
                "name": "Nokia",
                "description": "24 GB",
                "image": "",
                "category": category1,
                "price": 30000,
            },
            {
                "name": "Iphone",
                "description": "16GB",
                "image": "catalog/image/apple-dunyasindan-son-gelismeler-5.jpg",
                "category": category1,
                "price": 150000,
            },
        ]

        for product1_data in products1:
            product1, created = Product.objects.get_or_create(**product1_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added book: {product1.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Book already exists: {product1.name}")
                )

        category2, _ = Category.objects.get_or_create(
            name="Телевизоры",
            description="Стильный внешний вид, лучшая цветопередача, большая оперативная память и производительный процессор",
        )
        products2 = [
            {
                "name": "LG",
                "description": "QLED",
                "image": "",
                "category": category2,
                "price": 100000,
            },
            {
                "name": "DELL",
                "description": "QLED",
                "image": "",
                "category": category2,
                "price": 120000,
            },
        ]
        for product2_data in products2:
            product2, created = Product.objects.get_or_create(**product2_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added book: {product2.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Book already exists: {product2.name}")
                )
