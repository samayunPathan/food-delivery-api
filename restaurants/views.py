
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Restaurant, Menu, Category, MenuItem, Modifier
from .serializers import RestaurantSerializer, MenuSerializer, CategorySerializer, MenuItemSerializer, ModifierSerializer
from users.permissions import IsOwnerOrEmployee


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(pk=self.request.data['restaurant'])
        if self.request.user.is_owner or self.request.user.is_employee and self.request.user.restaurant == restaurant:
            serializer.save()
        else:
            raise permissions.PermissionDenied


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
