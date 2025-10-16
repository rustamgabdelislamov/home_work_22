from django.contrib import admin
from .models import Product, Category, Contacts


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "is_published")
    list_filter = ("category",)
    search_fields = ("name", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # Кортеж для отображения полей в списке


@admin.register(Contacts)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone")
    search_fields = ("name", "phone")