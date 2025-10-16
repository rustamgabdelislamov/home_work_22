from catalog.models import Category
from django.core.exceptions import ObjectDoesNotExist

def get_products_and_category_by_id(category_id):
    """
    Возвращает (queryset продуктов, объект категории) или вызывает исключение.
    """
    try:
        category = Category.objects.get(id=category_id) # в категорию идет категория которая находится под id который приходит с url
        products = category.products.all() # возвращает продукты которые в категории хранятся, т.к related_name = products
        return products, category # возвращаем кортеж с данными
    except ObjectDoesNotExist:
        raise ValueError(f"Category with ID {category_id} not found.")
