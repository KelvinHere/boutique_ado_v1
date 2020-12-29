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
        'stripe_public_key': 'pk_test_51I3lhpB6ymATCXs906ZAf2DlxOxad6H2kaiPOjEmTblXgUAE3J29D6MqGamQeVz842QwLEtpEGv5GwwCY0YcJyP600XVXyPZZv',
        'client_secret': 'fake secret key test',
    }

    return render(request, template, context)