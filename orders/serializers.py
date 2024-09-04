from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.serializers import MenuItemSerializer
from users.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'order_items', 'payment_method', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        restaurant = validated_data['restaurant']
        order = Order.objects.create(customer=user, restaurant=restaurant, **validated_data)
        return order