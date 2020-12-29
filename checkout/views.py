from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe

def checkout(request):
    # Setup stripe 'payment intent'
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Grab the bag session
    bag = request.session.get('bag', {})
    if not bag:
        # If no bag (user has input url manually) error message and redirect to products
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    # Grab current bag and get its grand total
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    # Convert total to integer for stripe
    stripe_total = round(total * 100)
    # Set secret key on stripe object
    stripe.api_key = stripe_secret_key
    # Create payment intent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing, did you forget to set it in your env?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)