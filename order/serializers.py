from rest_framework import serializers
from .models import Order, Cupon, OrderProduct
from django.utils import timezone

class OrderProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'count', 'price']
        read_only_fields = ['price']
    def create(self, validated_data):
        product = validated_data['product']
        validated_data['price'] = product.price
        return super().create(validated_data)



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderProductSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    cupon = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = [
            'id', 'phone_number', 'address', 'payment_type',
            'status', 'is_paid', 'order_items', 'total_price', 'created_at',
            'customer', 'cupon'
        ]
        read_only_fields = ['status', 'is_paid', 'created_at', 'customer']

    def get_total_price(self, obj):
        total = sum(item.count * item.price for item in obj.order_items.all())
        # Kupon chegirmasini qo‘llash
        if obj.cupon and obj.cupon.start_time <= timezone.now() <= obj.cupon.end_time:
            discount = (total * obj.cupon.discount_percentage) / 100
            return round(total - discount, 2)
        return total

    def create(self, validated_data):
        request = self.context.get('request')
        order_items_data = validated_data.pop('order_items')

        # 🔐 Avtomatik foydalanuvchi tayinlash
        validated_data['customer'] = request.user

        # 🎟️ Kuponni kod orqali olish
        cupon_code = validated_data.pop('cupon', None)
        cupon_obj = Cupon.objects.filter(code=cupon_code).first() if cupon_code else None

        # ⏳ Muddati tugagan kuponni rad etish
        if cupon_obj and not (cupon_obj.start_time <= timezone.now() <= cupon_obj.end_time):
            raise serializers.ValidationError({'cupon': 'Kupon muddati tugagan yoki mavjud emas.'})

        validated_data['cupon'] = cupon_obj

        order = Order.objects.create(**validated_data)

        # 📦 Har bir mahsulotni `OrderProduct` orqali saqlaymiz
        for item_data in order_items_data:
            product = item_data['product']
            count = item_data['count']

            if product.stock < count:
                raise serializers.ValidationError(f"{product.title} – zaxirada yetarli emas.")

            product.stock -= count
            product.save()

            OrderProduct.objects.create(
                order=order,
                product=product,
                count=count,
                price=product.price
            )

        self.send_confirmation_email(order)
        return order

    def send_confirmation_email(self, order):
        print(f"📧 Tasdiqlash xati yuborildi: Order ID {order.id}")


class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'
