from django.shortcuts import render

from orders_app.models import Shop
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


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
            cart.clear()
            return render(request,
                          'order_func/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'order_func/order/create.html',
                  {'cart': cart, 'form': form})