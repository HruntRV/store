from django.shortcuts import render
from products.models import Product, ProductCategory


def index(request):
    context = {
        'title': 'Test title',
        'username': 'valera',
    }
    return render(request, "products/index.html", context)


def products(request):
    context = {
        'title': 'Store - catalog',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, "products/products.html", context)
# Create your views here.
