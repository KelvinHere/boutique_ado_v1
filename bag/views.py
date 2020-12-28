from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    
    product = Product.objects.get(pk=item_id)


    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})  # Get bag session, if not create empty dict

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():    # Add quantity to existing
                bag[item_id]['items_by_size'][size] += quantity
            else:                                               #  Create new quantity for this size
                bag[item_id]['items_by_size'][size] = quantity
        else:                                                   # Item does not exist in bag create new dict to cater to different sizes
            bag[item_id] = {'items_by_size' : {size: quantity}}
    else:
        if item_id in list(bag.keys()): # Update quantity of existing
            bag[item_id] += quantity
        else:                           # Create new quantity for item
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag    # Update session with new quantity
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})  # Get bag session, if not create empty dict

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity  # Drill down to size dict and add quantity to that
            if not bag[item_id]['items_by_size']:
                bag.pop[item_id]
        else:
            del bag[item_id]['items_by_size'][size]
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag    # Update session with new quantity
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the specified product to the shopping bag """

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})  # Get bag session, if not create empty dict

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag    # Update session with new quantity
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)