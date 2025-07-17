from django.contrib import admin
from .models import Cupon, Order, OrderProduct

@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'start_time', 'end_time')
    search_fields = ('code',)
    list_filter = ('start_time', 'end_time')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'payment_type', 'status', 'created_at')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('customer__user__username', 'address')
    date_hierarchy = 'created_at'

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'count', 'price', 'created_at')
    list_filter = ('created_at',)
