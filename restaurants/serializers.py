from rest_framework import serializers
from .models import Restaurant, Menu, Category, MenuItem, Modifier


class ModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modifier
        fields = ['id', 'name', 'price', 'menu_item']
        read_only_fields = ['menu_item']


class MenuItemSerializer(serializers.ModelSerializer):
    modifiers = ModifierSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price',
                  'category', 'category_name', 'modifiers']
        read_only_fields = ['category']


class CategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    menu_name = serializers.ReadOnlyField(source='menu.name')

    class Meta:
        model = Category
        fields = ['id', 'name', 'menu', 'menu_name', 'menu_items']
        read_only_fields = ['menu']


class MenuSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Menu
        fields = ['id', 'name', 'restaurant', 'restaurant_name', 'categories']
        read_only_fields = ['restaurant']


class RestaurantSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'owner', 'menus']
        read_only_fields = ['owner']
