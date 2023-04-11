from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import Shop, Category, Product, ProductInfo, ProductParameter


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    model = Shop
    list_display = ['id', 'name', 'user']
    list_editable = ['name', 'user']


class ProductParameterInline(NestedStackedInline):
    model = ProductParameter


class ProductInfoInline(NestedStackedInline):
    model = ProductInfo
    inlines = [ProductParameterInline]


class ProductAdmin(NestedModelAdmin):
    model = Product
    list_display = ['id', 'name', 'category']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductInfoInline]


admin.site.register(Product, ProductAdmin)