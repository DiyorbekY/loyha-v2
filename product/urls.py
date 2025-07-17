from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .services import FlashSaleListCreateView,check_flash_sale,admin_replenish_stock,ProductViewHistoryCreate
from .views import *


router=DefaultRouter()
router.register(r'category',CategoryViewSet)
router.register(r'brand',BrandViewSet)
router.register(r'product',ProductViewSet)
router.register(r'review',ReviewViewSet)
router.register(r'wishlist',WishListViewSet)
router.register(r'flashsale',FlashSaleViewSet)

urlpatterns=[
    path('',include(router.urls)),

    path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
    path('check-sale/<int:product_id>/', check_flash_sale, name='product-view-history-create'),
    path('product-view/', ProductViewHistoryCreate.as_view(), name='product-view-history-create'),
    path('admin/replenish_stock/<int:product_id>/<int:amount>', admin_replenish_stock, name='admin_replenish_stock'),
]