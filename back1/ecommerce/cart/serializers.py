from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cart_items')
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'total']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.cart_items.all())