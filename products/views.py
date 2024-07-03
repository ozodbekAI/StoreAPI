from django.shortcuts import render
from rest_framework import viewsets
from .models import * 
from .serializers import * 
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartViewset(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Create or update CartItem
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemViewset(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)


class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            if cart.cartitem_set.exists():  # Cartda mahsulotlar mavjudligini tekshirish
                total_price = cart.total_price()
                
                order = Order.objects.create(user=user, total_price=total_price, status='pending')
                
                for cart_item in cart.cartitem_set.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )

                cart.cartitem_set.all().delete()  # Cartdagi barcha mahsulotlarni o'chirish
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Cart is empty. Cannot create order.'}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'detail': 'Cart does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]



class UserOrderHistoryViewset(viewsets.ModelViewSet):
    queryset = UserOrderHistory.objects.all()
    serializer_class = UserOrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
