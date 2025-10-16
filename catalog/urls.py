from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import CatalogListView, CatalogDetailView, CatalogCreateView, CatalogUpdateView, \
    CatalogDeleteView, CatalogContactsView, CategoryProductList

app_name = CatalogConfig.name

urlpatterns = [
    path("", CatalogListView.as_view(), name="product_list"),
    path("contacts/", CatalogContactsView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", (CatalogDetailView.as_view()), name="product_detail"),
    path("create_product/", CatalogCreateView.as_view(), name="create_product"),
    path("update_product/<int:pk>/", CatalogUpdateView.as_view(), name="update_product"),
    path("delete_product/<int:pk>/", CatalogDeleteView.as_view(), name="delete_product"),
    path("category_product/<int:category_id>/", CategoryProductList.as_view(), name="category_product"),

]
