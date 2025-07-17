from django.contrib import admin
from .models import Category, Brand, Product, Review, WishList, FlashSale

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'brand')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating')
    search_fields = ('user__username', 'product__title')
    list_filter = ('rating',)

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('product',)

@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
