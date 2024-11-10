from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

from store.models import Category, Subcategory, Product


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

    # Check for AJAX request and only render product list if true
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/_product_list.html', {'products': products})

    return render(request, 'store/category.html', {
        'category': category,
        'subcategories': subcategories,
        'products': products,
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

    # Paginate products
    paginator = Paginator(products, 30)  # Show 30 products per page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Check for AJAX request and only render product list if true
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'store/_product_list.html', {'products': products})

    return render(request, 'store/subcategory.html', {
        'category': category,
        'subcategory': subcategory,
        'products': products,
    })