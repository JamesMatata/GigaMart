from decimal import Decimal
from store.models import Product


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket')
        if 'basket' not in request.session:
            basket = self.session['basket'] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:
            # Increment quantity if product already exists in the basket
            self.basket[product_id]['qty'] = int(qty)
        else:
            # Add new product to the basket
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}
        self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:
            # Update the quantity of an existing product in the basket
            self.basket[product_id]['qty'] = int(qty)
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.basket:
            # Remove the product from the basket
            del self.basket[product_id]
        self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        """
        Returns all items in the basket as a list of dictionaries with each item’s details.
        """
        items = []
        for item in self:
            items.append(item)
        return items

    def get_subtotal(self):
        """
        Calculates the subtotal for all items in the basket.
        """
        return self.get_total_price()
