from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Avg, Count, F
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

# Import your models
try:
    from product.models import Product, Category, Brand, Review
    from order.models import Order, OrderItem
    from account.models import Customer
except ImportError:
    # Fallback if models don't exist yet
    Product = None
    Category = None
    Brand = None
    Review = None
    Order = None
    OrderItem = None
    Customer = None


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Category and Product and Brand:
            # Categories with product count
            context['categories'] = Category.objects.annotate(
                product_count=Count('product')
            )[:8]

            # Flash sale products
            context['flash_sale_products'] = Product.objects.filter(
                is_sale=True
            ).annotate(
                discount_percentage=((F('price') - F('sale_price')) / F('price') * 100)
            )[:8]

            # Featured products
            context['featured_products'] = Product.objects.annotate(
                average_rating=Avg('review__rating'),
                review_count=Count('review')
            ).order_by('-created_at')[:8]

            # Popular brands
            context['brands'] = Brand.objects.all()[:12]
        else:
            context['categories'] = []
            context['flash_sale_products'] = []
            context['featured_products'] = []
            context['brands'] = []

        return context


class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        if not Product:
            return []

        queryset = Product.objects.annotate(
            average_rating=Avg('review__rating'),
            review_count=Count('review')
        )

        # Search
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Brand filter
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand_id=brand)

        # Price filter
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        # Rating filter
        rating = self.request.GET.get('rating')
        if rating:
            queryset = queryset.filter(average_rating__gte=rating)

        # Sorting
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort == 'rating_desc':
            queryset = queryset.order_by('-average_rating')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Category and Brand:
            context['categories'] = Category.objects.annotate(
                product_count=Count('product')
            )
            context['brands'] = Brand.objects.all()
        else:
            context['categories'] = []
            context['brands'] = []
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        if Product:
            return Product.objects.all()
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Product and hasattr(self, 'object') and self.object:
            product = self.object

            # Related products
            context['related_products'] = Product.objects.filter(
                category=product.category
            ).exclude(id=product.id)[:4]

            # Product reviews
            if Review:
                context['reviews'] = Review.objects.filter(product=product).order_by('-created_at')

                # Average rating
                context['average_rating'] = Review.objects.filter(product=product).aggregate(
                    avg_rating=Avg('rating')
                )['avg_rating'] or 0
            else:
                context['reviews'] = []
                context['average_rating'] = 0
        else:
            context['related_products'] = []
            context['reviews'] = []
            context['average_rating'] = 0

        return context


class CategoryProductsView(ProductListView):
    def get_queryset(self):
        category_id = self.kwargs['pk']
        queryset = super().get_queryset()
        if queryset:
            return queryset.filter(category_id=category_id)
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Category:
            context['current_category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context


class BrandProductsView(ProductListView):
    def get_queryset(self):
        brand_id = self.kwargs['pk']
        queryset = super().get_queryset()
        if queryset:
            return queryset.filter(brand_id=brand_id)
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Brand:
            context['current_brand'] = get_object_or_404(Brand, pk=self.kwargs['pk'])
        return context


class ProductSearchView(ProductListView):
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query and Product:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(brand__name__icontains=query)
            ).annotate(
                average_rating=Avg('review__rating'),
                review_count=Count('review')
            )
        return []


class CartView(TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Cart items will be handled by JavaScript
        context['cart_items'] = []
        return context


class WishlistView(TemplateView):
    template_name = 'wishlist/wishlist.html'


class CheckoutView(TemplateView):
    template_name = 'checkout/checkout.html'


class FlashSalesView(ProductListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if queryset:
            return queryset.filter(is_sale=True)
        return []


class CategoriesView(ListView):
    template_name = 'categories/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        if Category:
            return Category.objects.annotate(product_count=Count('product'))
        return []


class BrandsView(ListView):
    template_name = 'brands/brands.html'
    context_object_name = 'brands'

    def get_queryset(self):
        if Brand:
            return Brand.objects.all()
        return []


class NewProductsView(ProductListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if queryset:
            return queryset.order_by('-created_at')
        return []


# User Authentication Views
class LoginView(AuthLoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True


class LogoutView(AuthLogoutView):
    next_page = 'home'


class RegisterView(TemplateView):
    template_name = 'auth/register.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'


class OrdersView(LoginRequiredMixin, ListView):
    template_name = 'account/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if Order and Customer:
            try:
                customer = Customer.objects.get(user=self.request.user)
                return Order.objects.filter(customer=customer)
            except Customer.DoesNotExist:
                return []
        return []


# AJAX Views
@method_decorator(csrf_exempt, name='dispatch')
class AddToCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)

            # Handle cart logic here
            return JsonResponse({'success': True, 'message': 'Mahsulot savatga qo\'shildi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class AddToWishlistView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')

            # Handle wishlist logic here
            return JsonResponse({'success': True, 'message': 'Mahsulot sevimlilar ro\'yxatiga qo\'shildi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')

            # Handle cart removal logic here
            return JsonResponse({'success': True, 'message': 'Mahsulot savatdan olib tashlandi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class UpdateCartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity')

            # Handle cart update logic here
            return JsonResponse({'success': True, 'message': 'Savatcha yangilandi'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class AddReviewView(View):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Tizimga kiring'})

        try:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            if Product and Customer and Review:
                product = get_object_or_404(Product, id=product_id)
                customer = get_object_or_404(Customer, user=request.user)

                Review.objects.create(
                    product=product,
                    customer=customer,
                    rating=rating,
                    comment=comment
                )

                messages.success(request, 'Sharhingiz qo\'shildi!')

            return redirect('product_detail', pk=product_id)
        except Exception as e:
            messages.error(request, 'Xatolik yuz berdi!')
            return redirect('product_detail', pk=product_id)