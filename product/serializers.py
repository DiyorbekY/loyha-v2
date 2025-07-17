from .models import Category,Brand,Product,Review,WishList,FlashSale
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields='__all__'

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model=Brand
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    avg_rating=serializers.FloatField(read_only=True,required=False)

    class Meta:
        model=Product
        fields=['id','category', 'brand', 'title', 'description', 'price', 'stock','is_active','avg_rating','image']

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Review
        fields='__all__'

class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model=WishList
        fields=['user','product']

class FlashSaleSerializer(serializers.ModelSerializer):

    class Meta:
        model=FlashSale
        fields='__all__'

class ProductViewHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields='__all__'
