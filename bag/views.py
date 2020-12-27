from django.shortcuts import render, redirect



def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})  # Get bag session, if not create empty dict

    if item_id in list(bag.keys()): # Update quantity of existing
        bag[item_id] += quantity
    else:                           # Create new quantity for item
        bag[item_id] = quantity

    request.session['bag'] = bag    # Update session with new quantity
    return redirect(redirect_url)