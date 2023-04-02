from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import Shop, Category, Product, ProductInfo, ProductParameter


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'slug']
#     list_editable = ['name']
#     prepopulated_fields = {'slug': ('name',)}
#
#
# class ProductParameterInline(admin.TabularInline):
#     model = ProductParameter
#
# working admin
# class ProductInfoInline(admin.TabularInline):
#     model = ProductInfo
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'category']
#     prepopulated_fields = {'slug': ('name',)}
#     inlines = [ProductInfoInline]


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