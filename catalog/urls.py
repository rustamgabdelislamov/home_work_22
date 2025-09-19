from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import CatalogListView,CatalogDetailView, CatalogCreateView, CatalogUpdateView, \
    CatalogDeleteView, CatalogContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path("", CatalogListView.as_view(), name="product_list"),
    path("contacts/", CatalogContactsView.as_view(), name="contacts"),
    path("product_detail/<int:pk>/", CatalogDetailView.as_view(), name="product_detail"),
    path("create_product/", CatalogCreateView.as_view(), name="create_product"),
    path("update_product/<int:pk>/", CatalogUpdateView.as_view(), name="update_product"),
    path("delete_product/<int:pk>/", CatalogDeleteView.as_view(), name="delete_product"),
]
