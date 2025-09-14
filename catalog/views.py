from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contacts


def home(request):  # Выборка последних 5 созданных продуктов
    latest_products = Product.objects.order_by("-created_at")[:5]

    # Вывод продуктов в консоль
    for product in latest_products:
        print(product.name)

    # Передача продуктов в шаблон
    return render(request, "catalog/home.html", {"latest_products": latest_products})
def home(request):# Выборка последних 5 созданных продуктов
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод продуктов в консоль
    for product in latest_products:
        print(product.name)

    # Передача продуктов в шаблон
    return render(request, 'catalog/home.html', {'latest_products': latest_products})


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # Создаем новый объект Contact и сохраняем его в базу данных
        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
    return render(request, "catalog/contacts.html")
