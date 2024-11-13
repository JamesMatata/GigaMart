from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from store.models import Product


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'account/dashboard/user_wish_list.html', {"wishlist": products})