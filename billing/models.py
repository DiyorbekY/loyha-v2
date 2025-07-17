from django.db import models
from order.models import Order

class Payments(models.Model):
    order=models.ForeignKey(Order,related_name='payments',on_delete=models.CASCADE)
    stripe_charge_id=models.CharField(max_length=50)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)