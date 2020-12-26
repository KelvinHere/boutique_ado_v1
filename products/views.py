from django.shortcuts import render
from .models import Product


def all_products(request):
    """ View to show all products, including sorting and searches """

    products = Product.objects.all()

    context = {
        'products' : products,
    }

    return render(request, 'products/products.html', context)
