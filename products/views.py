from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

# def index(request):
#     context = {
#         'title': 'Test title',
#         'username': 'valera',
#     }
#     return render(request, "products/index.html", context)


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - catalog'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/product.html'
    title = 'Store - item'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        product_id = self.kwargs.get('product_id')
        return queryset.filter(id=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context
# def products(request, category_id=None, page_number=1):
#     # if category_id:
#     #     category = ProductCategory.objects.get(id=category_id)
#     #     products = Product.objects.filter(category=category)
#     # else:
#     #     products = Product.objects.all()
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#     context = {
#         'title': 'Store - catalog',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator
#     }
#     return render(request, "products/products.html", context)
# Create your views here.


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
