from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache
from .forms import ProductForm, ProductModeratorForm
from .models import Product, Contacts, Category
from .services import get_products_and_category_by_id


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

    def get_queryset(self):
        # Получаем номер текущей страницы из GET-параметров
        page_number = self.request.GET.get('page', 1)
        cache_key = f'product_list_page_{page_number}'

        queryset = cache.get(cache_key)

        if not queryset:
            queryset = super().get_queryset()
            # Кэшируем данные, специфичные для этой страницы
            cache.set(cache_key, queryset, 60 * 15)  # 15 минут

        return queryset

class CategoryProductList(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = 'category_products'

    category_id = None

    def setup(self, request, *args, **kwargs):
        """Вызывается перед dispatch. Устанавливаем category_id."""
        super().setup(request, *args, **kwargs)
        self.category_id = self.kwargs.get('category_id')

    def get_queryset(self):
        """
        Теперь использует сервисный слой для получения продуктов.
        Если категория не найдена, возвращает пустой QuerySet.
        """
        if not self.category_id:
            return Product.objects.none()

        try:
            products, _ = get_products_and_category_by_id(self.category_id)
            return products
        except ValueError:
            # Если сервис выбросил ошибку (категория не найдена)
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 3. Получаем объект категории и добавляем его в контекст
        category_instance = None
        if self.category_id:
            try:
                # Пытаемся найти категорию
                category_instance = Category.objects.get(id=self.category_id)
            except Category.DoesNotExist:
                # Если категория не найдена (что соответствует вашему сообщению в шаблоне)
                pass

        context['category'] = category_instance

        # context['category_products'] уже установлен ListView
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
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
