import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from store.models import Product
from .Basket import Basket


class BasketSummaryView(View):
    def get(self, request):
        basket = Basket(request)
        basket_items = basket.get_items()  # Assuming `get_items()` returns the items in the basket
        basket_subtotal = basket.get_subtotal()  # Assuming `get_subtotal()` returns the subtotal
        return render(request, 'basket/summary.html', {
            'basket_items': basket_items,
            'basket_subtotal': basket_subtotal
        })


class BasketAddView(View):
    def post(self, request):
        basket = Basket(request)
        try:
            data = json.loads(request.body)  # Parse JSON data
            product_id = int(data.get('productid'))
            product_qty = int(data.get('productqty'))
            product = get_object_or_404(Product, id=product_id)
            basket.add(product=product, qty=product_qty)

            basket_qty = len(basket)
            return JsonResponse({'success': True, 'basket_qty': basket_qty})
        except (ValueError, KeyError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)


class BasketDeleteView(View):
    def post(self, request):
        basket = Basket(request)
        try:
            data = json.loads(request.body)
            product_id = int(data.get('productid'))  # Use data.get() for JSON
            product = get_object_or_404(Product, id=product_id)
            basket.delete(product=product)

            basket_qty = len(basket)
            basket_total = basket.get_total_price()
            return JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        except (ValueError, KeyError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)


class BasketUpdateView(View):
    def post(self, request):
        data = json.loads(request.body)  # Access JSON data correctly
        product_id = data.get('productid')
        product_qty = data.get('productqty')
        product = get_object_or_404(Product, id=product_id)

        # Proceed with updating the basket
        basket = Basket(request)
        basket.update(product=product, qty=product_qty)

        basket_qty = len(basket)
        basket_total = basket.get_total_price()
        return JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
