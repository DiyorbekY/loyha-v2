from django.db import models
from django_filters import rest_framework as django_filters

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.filters import ProductFilter
from product.schem import *
from product.serializers import *

from drf_spectacular.utils import extend_schema


class CustomPagination(PageNumberPagination):
    page_size = 4


@extend_schema(tags=['Product'])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['title', 'description']

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializer(related_products, many=True)
        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):

        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('avg_rating')[:3]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({'average_rating': 'No reviews yet!'})

        avg_rating = sum((review.rating for review in reviews)) / reviews.count()

        return Response({'average_rating': avg_rating})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    swagger_schema = CategorySchema
    permission_classes = [IsAuthenticated]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
    swagger_schema = BrandSchema
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    swagger_schema = ReviewSchema
    permission_classes = [IsAuthenticated]


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    swagger_schema = WishListSchema
    permission_classes = [IsAuthenticated]


class FlashSaleViewSet(viewsets.ModelViewSet):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSaleSerializer
    swagger_schema = FlashSaleSchema
    permission_classes = [IsAuthenticated]
