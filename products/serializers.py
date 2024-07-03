from rest_framework import serializers

from .models import *



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    cart_items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)

    def get_total_price(self, obj):
        return obj.total_price()

    def get_total_items(self, obj):
        return obj.total_items()




class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class UserOrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOrderHistory
        fields = '__all__'