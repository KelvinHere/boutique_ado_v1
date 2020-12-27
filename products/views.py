from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


def all_products(request):
    """ View to show all products, including sorting and searches """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        #  If get = sort (sort menu on main nav) sort by given criteria
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)  # Actually perform the sort


        # If get = category (category menus on main navbar) filter by given category/s
        if 'category' in request.GET:
            categories = request.GET['category'].split(',') # Split categories into list by ,
            products = products.filter(category__name__in=categories)  # Double underscoure common when query django
            categories = Category.objects.filter(name__in=categories)

        # If get = q (q = text input from search bar) filter by that given text
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didnt enter any search criteria")
                return redirect(reverse('products'))

            # | = OR : i befor contains means case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    # Things to pass to the page
    context = {
        'products' : products,
        'search' : query,
        'current_categories' : categories,
        'current_sorting' : current_sorting
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ View to show show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product' : product,
    }

    return render(request, 'products/product_detail.html', context)