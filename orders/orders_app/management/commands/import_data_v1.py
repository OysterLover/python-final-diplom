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

        # пополняем модель Shop
        Shop.objects.create(
            name=data['shop'],
            filename=file_name,)

        # пополняем модель Category
        for item in data['categories']:
            Category.objects.create(
                id=item['id'],
                name=item['name'],
                #shops= как указать ссылку на объект shop который создаем выше, если поле m2m?
            )

        # пополняем модель Product
        for item in data['goods']:
            Product.objects.create(
                id=item['id'],
                category=item['category'],# как указать ссылку на объект Category который создаем выше, если поле foreign key?
            )

        # пополняем модель ProductInfo
        for item in data['goods']:
            ProductInfo.objects.create(
                # product= как указать ссылку на объект Category который создаем выше, если поле foreign key?
                # shop= как указать ссылку на объект Shop который создаем выше, если поле foreign key?
                # name = как протащить его сюда
                model=item['model'],
                quantity=item['quantity'],
                price=item['price'],
                price_rrc=item['price_rrc']
            )

        # пополняем модель Parameter, ProductParameter
        for item in data['goods']:

            params_dict = item['parameters']
            for parameter in list(params_dict.keys()):
                Parameter.objects.create(
                    name=parameter
                )

                ProductParameter.objects.create(
                    # product_info = как протащить сюда параметр из объекта ProductInfo сверху
                    # parameter = как протащить сюда параметр из объекта Parameter сверху
                    value=params_dict[parameter]
                )

