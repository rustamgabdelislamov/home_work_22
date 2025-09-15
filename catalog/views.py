from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Contacts
from .forms import ProductForm
from django.core.paginator import Paginator


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # Создаем новый объект Contact и сохраняем его в базу данных
        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
    return render(request, "catalog/contacts.html")


def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3)  # 10 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/home.html', {'page_obj': page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product,pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})





