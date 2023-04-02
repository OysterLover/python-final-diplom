from django.db import models
from django.urls import reverse
from django.utils.text import slugify

STATUS_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)


class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')
    email = models.EmailField(max_length=70, blank=True, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class Shop(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    user = models.OneToOneField(User, verbose_name='Пользователь',
                                blank=True, null=True,
                                on_delete=models.CASCADE)
    filename = models.CharField(max_length=50, verbose_name='Filename')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)
    name = models.CharField(max_length=40, verbose_name='Название')
    slug = models.SlugField(max_length=200, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders_app:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name='Название')
    slug = models.SlugField(max_length=200, null=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Список продуктов"
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders_app:product_detail', args=[self.id, self.slug])


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='product_infos', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', blank=True,
                             on_delete=models.CASCADE)
    model = models.CharField(max_length=80, verbose_name='Модель')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = "Информационный список о продуктах"


class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Список имен параметров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
                                     related_name='product_parameters', blank=True,
                                     on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"


# class Order(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь',
#                              related_name='orders', blank=True,
#                              on_delete=models.CASCADE)
#     dt = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, max_length=15)
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = "Список заказов"
#         ordering = ('-dt',)
#
#     def __str__(self):
#         return str(self.dt)
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
#                               on_delete=models.CASCADE)
#     product = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', related_name='ordered_items',
#                                 blank=True,
#                                 on_delete=models.CASCADE)
#     shop = models.ForeignKey(Shop, verbose_name="Магазин", related_name='ordered_items', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(verbose_name='Количество')
#
#     class Meta:
#         verbose_name = 'Заказанная позиция'
#         verbose_name_plural = "Список заказанных позиций"
#
#
# class Contact(models.Model):
#     address = models.CharField(verbose_name='Адрес', max_length=200)
#     user = models.ForeignKey(User, verbose_name='Пользователь',
#                              related_name='contacts', blank=True,
#                              on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Контакты пользователя'
#         verbose_name_plural = "Список контактов пользователя"
