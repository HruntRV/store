from django.urls import path

from products.views import (ProductListView, ProductsListView, basket_add,
                            basket_remove)

# from products.views import products

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),  # путь для отображения всех товаров
    # path('category/<int:category_id>/', products, name='category'),  # путь для отображения товаров конкретной категории
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    # path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('<int:product_id>/', ProductListView.as_view(), name='product'),

]

