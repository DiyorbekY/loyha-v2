from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuponViewSet, OrderViewSet, OrderProductViewSet, PlaceOrderAPIView

router = DefaultRouter()
router.register(r'cupon', CuponViewSet)
router.register(r'order', OrderViewSet)
router.register(r'orderproduct', OrderProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('place_order/', PlaceOrderAPIView.as_view(), name='place_order'),

]
