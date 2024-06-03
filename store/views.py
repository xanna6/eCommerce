import json

from django.shortcuts import render
from .models import *
from django.http import JsonResponse


def products(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        orderItems = order['get_cart_items']

    product_list = Product.objects.all()
    context = {'products': product_list, 'cartItems': orderItems}
    return render(request, 'products.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        orderItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': orderItems}
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        orderItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        orderItems = order['get_cart_items']

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
        customerInfo = Customer()
        customerInfo.name = request.POST['name']
        customerInfo.email = request.POST['email']
        print(customerInfo)

    return JsonResponse('Order completed', safe=False)
