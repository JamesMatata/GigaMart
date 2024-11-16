import urllib.parse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from basket.Basket import Basket
from store.models import Category, Subcategory, Product, Inquiry, CheckoutSession, Order


def index(request):
    top_traded_products = Product.objects.all().order_by('-traded_count')[:5]
    return render(request, 'store/index.html', {'top_traded_products': top_traded_products})


def get_subcategories(request, category_id):
    category = Category.objects.get(pk=category_id)
    subcategories = Subcategory.objects.filter(category=category).values('id', "name")
    return JsonResponse(list(subcategories), safe=False)


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Subcategory.objects.filter(category=category)
    products = Product.objects.filter(category=category)

    # Apply filters only if parameters are provided
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    subcategory_slugs = request.GET.getlist('subcategory')  # Get selected subcategory slugs
    discount = request.GET.get('discount')
    availability = request.GET.get('availability')
    warranty_months = request.GET.getlist('warranty')
    arrival = request.GET.get('arrival')

    if price_min and price_max:
        products = products.filter(price__gte=price_min, price__lte=price_max)

    # Apply filter for subcategories by their slugs
    if subcategory_slugs:
        products = products.filter(subcategory__slug__in=subcategory_slugs)  # Filter by slug, not id

    if discount:
        products = products.filter(discount__gte=discount)

    if availability == 'in_stock':
        products = products.filter(items_remaining__gt=0)

    if warranty_months:
        products = products.filter(warrant_months__in=warranty_months)

    if arrival == 'newest':
        products = products.order_by('-id')

    # Pagination settings
    paginator = Paginator(products, 1)  # Adjust items per page as needed
    page_number = request.GET.get('page')

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    # Return partial template if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/_product_list.html', {'products': paginated_products})

    return render(request, 'store/category.html', {
        'category': category,
        'subcategories': subcategories,
        'products': paginated_products,
        'page_obj': paginated_products
    })


def search_results(request):
    query = request.GET.get('searchbar_input', '').strip()

    # Start with an empty queryset
    products = Product.objects.none()

    if query:
        # Filter products by search query in name and description
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

        print(products)
        # Apply additional filters
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        subcategory_slugs = request.GET.getlist('subcategory')
        discount = request.GET.get('discount')
        availability = request.GET.get('availability')
        warranty_months = request.GET.getlist('warranty')
        arrival = request.GET.get('arrival')

        if price_min and price_max:
            products = products.filter(price__gte=price_min, price__lte=price_max)

        if subcategory_slugs:
            products = products.filter(subcategory__slug__in=subcategory_slugs)

        if discount:
            products = products.filter(discount__gte=discount)

        if availability == 'in_stock':
            products = products.filter(items_remaining__gt=0)

        if warranty_months:
            products = products.filter(warrant_months__in=warranty_months)

        if arrival == 'newest':
            products = products.order_by('-id')

        # Pagination
        paginator = Paginator(products, 10)  # Adjust items per page as needed
        page_number = request.GET.get('page')

        try:
            paginated_products = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)
        print(paginated_products)
        # Check if AJAX request for dynamic loading
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print('start')
            print(products)
            print('finish')
            return render(request, 'store/_product_list.html', {'products': paginated_products})
        print(products)
        return render(request, 'store/search.html', {
            'query': query,
            'products': paginated_products,
            'page_obj': paginated_products
        })
    else:
        return render(request, 'store/search.html', {
            'query': query,
            'products': [],
            'page_obj': []
        })


def subcategory_list(request, category_slug, subcategory_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        subcategory = Subcategory.objects.get(slug=subcategory_slug, category=category)
    except (Category.DoesNotExist, Subcategory.DoesNotExist):
        raise Http404("Subcategory or Category does not exist")

    products = Product.objects.filter(subcategory=subcategory)

    # Apply filters only if parameters are provided
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    discount = request.GET.get('discount')
    availability = request.GET.get('availability')
    warranty_months = request.GET.getlist('warranty')
    arrival = request.GET.get('arrival')

    if price_min and price_max:
        products = products.filter(price__gte=price_min, price__lte=price_max)

    if discount:
        products = products.filter(discount__gte=discount)

    if availability == 'in_stock':
        products = products.filter(items_remaining__gt=0)

    if warranty_months:
        products = products.filter(warrant_months__in=warranty_months)

    if arrival == 'newest':
        products = products.order_by('-id')

    # Pagination settings
    paginator = Paginator(products, 1)  # Adjust items per page as needed
    page_number = request.GET.get('page')

    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    # Return partial template if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/_product_list.html', {'products': paginated_products})

    return render(request, 'store/subcategory.html', {
        'category': category,
        'subcategory': subcategory,
        'products': paginated_products,
        'page_obj': paginated_products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'store/product_page.html', context)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.users_wishlist.all():
        # If the product is already in the wishlist, remove it
        product.users_wishlist.remove(request.user)
        return JsonResponse({'status': 'removed', 'message': 'Product removed from wishlist'})
    else:
        # Add the product to the user's wishlist
        product.users_wishlist.add(request.user)
        return JsonResponse({'status': 'added', 'message': 'Product added to wishlist'})


def remove_from_wishlist(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            # Remove the product from the user's wishlist
            product.users_wishlist.remove(request.user)

            # Get the count of products in the user's wishlist
            wishlist_count = product.users_wishlist.count()

            # Return the response with the new wishlist count
            return JsonResponse({
                'status': 'removed',
                'message': 'Product removed from wishlist',
                'wishlist_count': wishlist_count  # Send the updated wishlist count
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def checkout_view(request):
    checkout_session = None

    # Check if the user is authenticated and retrieve or create the CheckoutSession
    if request.user.is_authenticated:
        checkout_session, created = CheckoutSession.objects.get_or_create(user=request.user)
    else:
        # If the user is not authenticated, create a guest session (optional)
        checkout_session, created = CheckoutSession.objects.get_or_create(user=None)

    # Get basket details
    basket = Basket(request)
    basket_items = basket.get_items()  # Fetch items in basket
    basket_subtotal = basket.get_subtotal()

    # Handle POST requests for form submissions
    if request.method == 'POST':
        if request.POST.get('back'):
            # Handle back navigation
            if checkout_session.step == 'confirm':
                checkout_session.step = 'details'
            elif checkout_session.step == 'details':
                checkout_session.step = 'summary'
        else:
            # Move to the next step and save user data
            if checkout_session.step == 'summary':
                checkout_session.step = 'details'
            elif checkout_session.step == 'details':
                # Save the form data into the session model
                checkout_session.first_name = request.POST.get('first_name', checkout_session.first_name)
                checkout_session.last_name = request.POST.get('last_name', checkout_session.last_name)
                checkout_session.email = request.POST.get('email', checkout_session.email)
                checkout_session.phone = request.POST.get('phone', checkout_session.phone)
                checkout_session.county = request.POST.get('county', checkout_session.county)
                checkout_session.save()  # Save data to the database
                checkout_session.step = 'confirm'

            elif checkout_session.step == 'confirm':
                # Create Inquiry and fill details from the session and basket items
                inquiry = Inquiry.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=f"{checkout_session.first_name} {checkout_session.last_name}",
                    email=checkout_session.email,
                    items=[{
                        'product_id': item['product'].id,
                        'product_name': item['product'].name,
                        'qty': item['qty'],
                        'price': str(item['price'])
                    } for item in basket_items],
                    inquiry_status='Pending',
                    inquiry_whatsapp_link='',  # Initially, it can be an empty string
                )

                # Construct WhatsApp URL for the inquiry
                # Construct WhatsApp URL for the inquiry (encode the message properly)
                message = f"Hello, I am {checkout_session.first_name} {checkout_session.last_name}, from {checkout_session.county}, inquiry id: {inquiry.unique_id}, I am interested in these products:"
                message += ' | '.join(
                    [f"{item['qty']} {item['product'].name} @ {item['price']}" for item in basket_items]
                )
                message += ". How can I get them?"

                # URL-encode the message
                encoded_message = urllib.parse.quote_plus(message)

                # Final WhatsApp URL
                whatsapp_url = f"https://wa.me/?text={encoded_message}"

                # Set the WhatsApp link in the Inquiry object
                inquiry.inquiry_whatsapp_link = whatsapp_url
                inquiry.save()

                # Delete the checkout session after completing the process
                checkout_session.delete()

                # Redirect to the WhatsApp URL for the inquiry
                return redirect(whatsapp_url)

        checkout_session.save()  # Save after changes

    # Render the checkout page with the current step and user data
    return render(request, 'store/checkout.html', {
        'step': checkout_session.step,
        'user_data': {
            'first_name': checkout_session.first_name,
            'last_name': checkout_session.last_name,
            'email': checkout_session.email,
            'phone': checkout_session.phone,
            'county': checkout_session.county,
        },
        'basket_items': [{
            'product_name': item['product'].name,
            'qty': item['qty'],
            'price': str(item['price']),
        } for item in basket_items],
        'basket_subtotal': str(basket_subtotal),
    })


def inquiries_view(request):
    context = {}

    if request.user.is_authenticated:
        # Get inquiries for the authenticated user
        inquiries = Inquiry.objects.filter(user=request.user).order_by('-created_at')
        context['inquiries'] = inquiries
    else:
        # Add a message for unauthenticated users
        context = {}

    return render(request, 'store/inquiries.html', context)


def orders_view(request):
    context = {}

    if request.user.is_authenticated:
        # Get inquiries for the authenticated user
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        context['orders'] = orders
    else:
        context = {}

    return render(request, 'store/orders.html', context)


def get_inquiry(request):
    inquiry_id = request.GET.get('inquiry_id')
    inquiry = Inquiry.objects.filter(unique_id=inquiry_id).first()

    if inquiry:
        # Render the partial template with the inquiry data
        html = render_to_string('store/_inquiry_card.html', {'inquiry': inquiry})
        return JsonResponse({'html': html})
    else:
        return JsonResponse({'html': '<p>Inquiry not found.</p>'})


def get_order(request):
    order_id = request.GET.get('inquiry_id')
    order = Order.objects.filter(unique_id=order_id).first()

    if order:
        # Render the partial template with the inquiry data
        html = render_to_string('store/_order_card.html', {'order': order})
        return JsonResponse({'html': html})
    else:
        return JsonResponse({'html': '<p>Order not found.</p>'})
