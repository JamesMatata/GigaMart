from django import template

register = template.Library()

@register.filter
def in_basket(product, basket):
    """Check if a product is in the basket."""
    return any(item['product'].id == product.id for item in basket.get_items())
