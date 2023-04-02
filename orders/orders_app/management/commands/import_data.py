import yaml
from yaml.loader import SafeLoader
from pytils.translit import slugify

from django.core.management.base import BaseCommand
from orders_app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file_name = 'shop1.yaml'
        with open(file_name, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=SafeLoader)

        shop, _ = Shop.objects.update_or_create(name=data['shop'],)

        for item in data['categories']:
            category, _ = Category.objects.update_or_create(
                id=item['id'],
                name=item['name'],
                slug=slugify(item['name'])
            )
            category.shops.add(shop.id)
            category.save()

        for item in data['goods']:
            product, _ = Product.objects.update_or_create(
                id=item['id'],
                category_id=item['category'],
                name=item['name'],
                slug=slugify(item['name'])

            )

            product_info, _ = ProductInfo.objects.update_or_create(
                product_id=product.id,
                shop_id=shop.id,
                model=item['model'],
                quantity=item['quantity'],
                price=item['price'],
                price_rrc=item['price_rrc']
            )

            for name, value in item['parameters'].items():
                parameter, _ = Parameter.objects.update_or_create(name=name)
                ProductParameter.objects.create(product_info_id=product_info.id,
                                                parameter_id=parameter.id,
                                                value=value)