from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.models import MenuItem
from restaurants.serializers import MenuItemSerializer, RestaurantSerializer
from users.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), write_only=True, source='menu_item'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'order_items',
                  'payment_method', 'total_amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user',
                            'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        total_amount = 0
        for item_data in order_items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            OrderItem.objects.create(
                order=order, menu_item=menu_item, quantity=quantity)
            total_amount += menu_item.price * quantity

        order.total_amount = total_amount
        order.save()
        return order
