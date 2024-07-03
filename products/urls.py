from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewset, basename="products")
router.register(r'categories', CategoryViewset, basename="categories")
router.register(r'tags', TagViewset, basename="tags")
router.register(r'cart', CartViewset, basename='cart')
router.register(r'cart_items', CartItemViewset, basename='cartitem')
router.register(r'order', OrderViewset, basename='order')
router.register(r'order_items', OrderItemViewset, basename='orderitem')
router.register(r'user_order_history', UserOrderHistoryViewset, basename='user_order_history')


urlpatterns = [
    path('', include(router.urls))
]