import yaml
from yaml.loader import SafeLoader

from django.core.management.base import BaseCommand
from orders.orders_app.models import Shop, Category, Product, ProductInfo, Parameter, \
    ProductParameter


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        file_name = 'shop1.yaml'
        with open(file_name, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=SafeLoader)

        shop = Shop.objects.create(name=data['shop'],)

        for item in data['categories']:
            category = Category.objects.create(
                id=item['id'],
                name=item['name'],
            )
            category.shops.add(shop.id)

        for item in data['goods']:
            product = Product.objects.create(
                id=item['id'],
                category=item['category'],
                #достаточно ли этого для category, если это foreign key?
            )

            product_info = ProductInfo.objects.create(
                product=product.id,
                shop=shop.id,
                name=product.name,
                model=item['model'],
                quantity=item['quantity'],
                price=item['price'],
                price_rrc=item['price_rrc']
            )

            for name, value in item['parameters'].items():
                parameter = Parameter.objects.create(name=name)
                ProductParameter.objects.create(product_info=product_info.id,
                                                parameter=parameter.id,
                                                value=value)