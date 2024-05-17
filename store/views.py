from django.shortcuts import render
from .models import *


def products(request):
    product_list = Product.objects.all()
    context = {'products': product_list}
    return render(request, 'products.html', context)


def cart(request):
    return render(request, 'cart.html')
