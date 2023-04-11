from django.shortcuts import render

from orders_app.models import Shop
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                shop = Shop.objects.get(name=item['shop'])
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         shop=shop)

                # Send mail to buyer

                subject = 'Уведомление о заказе'
                message = f'Ваш заказ: {item["product"]}\n' \
                          f'Количество: {item["quantity"]}\n' \
                          f'Общей стоимостью: ₽{item["quantity"]*item["price"]}\n' \
                          f'Адрес доставки: {order.address}'
                from_email = 'olesynikitina@gmail.com'
                to_email = order.email

                send_mail(
                    subject,
                    message,
                    from_email,
                    [to_email],
                    fail_silently=False,
                )

                # Send mail to seller

                subject_2 = 'Уведомление о заказе в вашем магазине'
                message_2 = f'Заказанный продукт: {item["product"]}\n' \
                          f'Количество: {item["quantity"]}\n' \
                          f'Общей стоимостью: ₽{item["quantity"] * item["price"]}\n' \
                          f'Адрес доставки: {order.address}'
                from_email_2 = 'olesynikitina@gmail.com'

                shop = Shop.objects.get(name=item['shop'])
                to_email_2 = shop.user.email

                send_mail(
                    subject_2,
                    message_2,
                    from_email_2,
                    [to_email_2],
                    fail_silently=False,
                )

            cart.clear()
            return render(request,
                          'order_func/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'order_func/order/create.html',
                  {'cart': cart, 'form': form})