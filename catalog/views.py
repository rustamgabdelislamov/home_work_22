from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, ProductModeratorForm
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


class CatalogDetailView(LoginRequiredMixin, DetailView):
    model = Product


class CatalogCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')


    def form_valid(self, form):
        """Присваиваем при создании продукта id создателя"""

        form.instance.owner = self.request.user
            # Сохраняем объект
        return super().form_valid(form)


class CatalogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    permission_required = 'catalog.can_unpublish_product'

    def get_form_class(self):
        user = self.request.user # Извлекает объект текущего аутентифицированного пользователя из объекта запроса (self.request), связанного с текущим представлением/контекстом. |
        if user == self.object.owner: # Проверяет, совпадает ли текущий user с атрибутом owner объекта, который создается автоматически при создании продукта
            return ProductForm #  если совпадает owner создателя, то полная форма для редактирования
        if user.has_perm("catalog.can_unpublish_product"): # если только через разрешение, то неполная форма
            return ProductModeratorForm
        raise PermissionDenied


class CatalogDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    permission_required = "catalog.delete_product"

    def get_object(self, queryset=None):
        """
        Разрешает удаление, если пользователь является владельцем ИЛИ модератором.
        """
        obj = super().get_object(queryset)

        # Проверка 1: Является ли пользователь владельцем объекта?
        is_owner = (self.request.user == obj.owner)

        # Проверка 2: Имеет ли пользователь право модератора?
        has_moderator_permission = self.request.user.has_perm(self.permission_required)

        if is_owner or has_moderator_permission:
            return obj
        raise PermissionDenied
