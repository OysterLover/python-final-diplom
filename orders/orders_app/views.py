from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Category, ProductInfo, Product
from .serializers import ProductInfoSerializer
from cart.forms import CartAddProductForm


# class ProductInfoViewSet(ModelViewSet):
#     queryset = ProductInfo.objects.all()
#     serializer_class = ProductInfoSerializer

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'orders_app/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'orders_app/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


