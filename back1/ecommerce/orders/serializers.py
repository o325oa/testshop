from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email',
            'address', 'postal_code', 'city', 'country', 'phone',
            'created', 'updated', 'status', 'paid', 'payment_method',
            'total', 'transaction_id', 'items'
        ]
        read_only_fields = ['user', 'created', 'updated', 'total']