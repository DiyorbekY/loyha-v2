from django.core.exceptions import ValidationError
from order.models import Order

def place_order(product,customer,count):
    if product and customer and count > 0:
        order=Order(product=product,customer=customer,count=count)
        order.save()
        return order
    else:
        raise ValidationError('Buyurtma parametrlari yaroqsiz.')