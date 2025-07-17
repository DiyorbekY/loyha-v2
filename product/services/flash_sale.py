from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,generics,serializers
from datetime import datetime,timedelta
from product.models import Product,ProductViewHistory,FlashSale
from django.utils import timezone


class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = ('id', 'product', 'discount_percentage', 'start_time', 'end_time')
            ref_name = 'FlashSaleInlineSerializer'

    serializer_class = FlashSaleSerializer

@api_view(['GET'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()

    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=timezone.now() + timedelta(hours=24)
    ).first()

    if user_viewed and upcoming_flash_sale:
        return Response({
            'message': f'Bu mahsulot {upcoming_flash_sale.discount_percentage}% chegirmaga ega',
            'start_time': upcoming_flash_sale.start_time,
            'end_time': upcoming_flash_sale.end_time
        })
    return Response({'message': 'Yaqin kunlarda bu mahsulotga chegirma yo‘q'})