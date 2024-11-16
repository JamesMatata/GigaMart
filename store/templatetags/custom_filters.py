from django import template

register = template.Library()


@register.filter
def render_specification(value):
    """Recursively renders a nested dictionary as HTML."""
    if isinstance(value, dict):
        html = "<ul>"
        for key, val in value.items():
            html += f"<li><strong>{key}:</strong> {render_specification(val)}</li>"
        html += "</ul>"
        return html
    else:
        return value


@register.filter
def total_price(items):
    total = 0
    for item in items:
        total += float(item.get('qty', 0)) * float(item.get('price', 0))
    return total
