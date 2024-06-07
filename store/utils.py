import json

from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    orderItems = order['get_cart_items']

    for i in cart:
        try:
            orderItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
        except:
            pass
    return {'orderItems': orderItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        orderItems = cookieData['orderItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'orderItems': orderItems, 'order': order, 'items': items}


def guestOrder(request):
    print('Cookies: ', request.COOKIES)
    name = request.POST['name']
    email = request.POST['email']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    cookieData = cookieCart(request)
    items = cookieData['items']
    order = Order.objects.create(
        customer=customer,
        completed=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order
