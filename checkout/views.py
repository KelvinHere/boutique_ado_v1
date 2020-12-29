from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    # Grab the bag session
    bag = request.session.get('bag', {})
    if not bag:
        # If no bag (user has input url manually) error message and redirect to products
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'

    context = {
        'order_form': order_form,
    }

    return render(request, template, context)