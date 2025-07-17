from django.db.models.signals import post_save
from django.dispatch import receiver
from order.models import OrderProduct

@receiver(post_save, sender=OrderProduct)
def reduce_stock_on_save(sender, instance, created, **kwargs):
    if created:
        instance.product.stock -= instance.count
        instance.product.save()