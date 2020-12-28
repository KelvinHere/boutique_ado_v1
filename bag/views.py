from django.shortcuts import render, redirect



def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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

    request.session['bag'] = bag    # Update session with new quantity
    return redirect(redirect_url)