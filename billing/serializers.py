from product.models import Product


def calculate_total(order_items):
    total = 0
    for item in order_items:
        product = Product.objects.get(id=item['product'])
        total += product.price * item['count']
    return total