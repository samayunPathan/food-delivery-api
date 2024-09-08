from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Restaurant, Menu, Category, MenuItem, Modifier
from .serializers import RestaurantSerializer, MenuSerializer, CategorySerializer, MenuItemSerializer, ModifierSerializer
from users.permissions import IsOwnerOrEmployee
from rest_framework.exceptions import ValidationError


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        name = self.request.data.get('name')
        address = self.request.data.get('address')

        # Check a restaurant with the same name and address already exists
        if Restaurant.objects.filter(name=name, address=address).exists():
            raise ValidationError(
                f"A restaurant with the name '{name}' and address '{address}' already exists.")

        # If no duplicate proceed creation
        serializer.save(owner=self.request.user)


class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        if not restaurant_id:
            raise ValidationError(
                "Restaurant ID is required to create a menu.")

        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise ValidationError(
                f"Restaurant with id {restaurant_id} does not exist.")

        if self.request.user.is_owner or (self.request.user.is_employee and self.request.user.restaurant == restaurant):
            serializer.save(restaurant=restaurant)
        else:
            raise permissions.PermissionDenied(
                "You don't have permission to create a menu for this restaurant.")


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        menu = Menu.objects.get(pk=self.request.data['menu'])
        if self.request.user.is_owner or self.request.user.is_employee and self.request.user.restaurant == menu.restaurant:
            serializer.save()
        else:
            raise permissions.PermissionDenied


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        category = Category.objects.get(pk=self.request.data['category'])
        if self.request.user.is_owner or self.request.user.is_employee and self.request.user.restaurant == category.menu.restaurant:
            serializer.save()
        else:
            raise permissions.PermissionDenied


class ModifierListCreateView(generics.ListCreateAPIView):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        menu_item = MenuItem.objects.get(pk=self.request.data['menu_item'])
        if self.request.user.is_owner or self.request.user.is_employee and self.request.user.restaurant == menu_item.category.menu.restaurant:
            serializer.save()
        else:
            raise permissions.PermissionDenied
