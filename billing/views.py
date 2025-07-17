from django.shortcuts import render

from rest_framework import views,status
from rest_framework.response import Response
import stripe
from django.conf import settings
from .models import Payments
from order.models import Order
from product.models import Product

stripe.api_key=settings.STRIPE_SECRET_KEY

class CreateChargeView(views.APIView):
    def post(self,request,*args,**kwargs):
        stripe_token=request.data.get('stripe_token')
        order_id=request.data.get('order_id')

        try:
            order=Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error':'Order topilmadi'},status=status.HTTP_400_BAD_REQUEST)
        try:
            total_amount = sum([
                item.price * item.count
                for item in order.order_items.all()
            ])
            charge=stripe.Charge.create(
                amount=int(total_amount*100),
                currency='usd',
                source=stripe_token
            )
            Payments.objects.create(
                order=order,
                stripe_charge_id=charge['id'],
                amount=total_amount
            )
            order.is_paid=True
            order.save()

            return Response({'status':"To'lov muvaffaqiyatli o'tdi"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':f"Xatolik bo'lyabdi {str(e)}"},status=status.HTTP_400_BAD_REQUEST)