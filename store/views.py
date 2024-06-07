import json

from django.shortcuts import render
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse


def products(request):
    data = cartData(request)
    orderItems = data['orderItems']

    product_list = Product.objects.all()
    context = {'products': product_list, 'cartItems': orderItems}
    return render(request, 'products.html', context)


def cart(request):
    data = cartData(request)
    orderItems = data['orderItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': orderItems}
    return render(request, 'cart.html', context)


def checkout(request):
    data = cartData(request)
    orderItems = data['orderItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': orderItems}
    return render(request, 'checkout.html', context)


def updateCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId:', productId)
    print('Action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added to cart', safe=False)


def processOrder(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
        else:
            customer, order = guestOrder(request)

        order.completed = True
        order.save()

        ShippingData.objects.create(
            order=order,
            address=request.POST['address'],
            postalCode=request.POST['postal-code'],
            city=request.POST['city'],
            country=request.POST['country']
        )

    context = {'cartItems': 0}
    response = render(request, 'summary.html', context)
    response.delete_cookie('cart')
    return response
