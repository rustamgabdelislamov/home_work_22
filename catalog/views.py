from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product, Contacts


class CatalogContactsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'catalog/contacts.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # Создаем новый объект Contact и сохраняем его в базу данных
        Contacts.objects.create(name=name, phone=phone, message=message)
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")


class CatalogListView(ListView):
    model = Product
    paginate_by = 3


class CatalogDetailView(DetailView):
    model = Product


class CatalogCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')


class CatalogUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')


class CatalogDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')
