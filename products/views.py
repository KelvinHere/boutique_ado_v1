from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


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
            if sortkey == 'category':
                sortkey = 'category__name'

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
        'search_term' : query,
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


@login_required
def add_product(request):
    """ Add a product to the store """
    # Redirect home if not a superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Ready to accept files
        if form.is_valid():
            product = form.save()  # Drop form into product then we can get product.id to redirect later
            messages.success(request, 'Successfully added product')            
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product.  Please enure the form is valid')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = { 
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    # Redirect home if not a superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)  # Get the product from id
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product.  Please ensure the form is valid.')
    else: #If request method is GET
        form = ProductForm(instance=product)  # Instanciate a form from the product
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = { 
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    # Redirect home if not a superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)  # Get product
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


