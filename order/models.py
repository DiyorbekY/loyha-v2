
from django.db import models
from product.models import Product
from django.contrib.auth.models import User

class Cupon(models.Model):
    code=models.CharField(max_length=20,unique=True,blank=True,null=True)
    discount_percentage=models.PositiveIntegerField()
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()

    def __str__(self):
        return self.code

class Order(models.Model):

    PAYMENT_CHOICES = (
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('transfer', 'Bank Transfer'),
    )

    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    phone_number=models.CharField(max_length=13)
    address = models.TextField()
    cupon = models.ForeignKey(Cupon, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False, null=True)



    def set_status(self,new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError('Yaroqsiz status')

        self.status=new_status
        self.save()

    def is_transition_allowed(self,new_status):
        allowed_transitions={
            self.PENDING:[self.PROCESSING,self.CANCELED],
            self.PROCESSING:[self.SHIPPED,self.CANCELED],
            self.SHIPPED:[self.DELIVERED,self.CANCELED]
        }
        return new_status in allowed_transitions.get(self.status,[])
    def __str__(self):
        return f"Order({self.id} by {self.customer.user.username})"

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} x {self.count}"


