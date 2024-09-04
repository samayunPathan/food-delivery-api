from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Restaurant, Menu, Category, MenuItem, Modifier
from .serializers import RestaurantSerializer, MenuSerializer, CategorySerializer, MenuItemSerializer, ModifierSerializer
from users.permissions import IsOwnerOrEmployee


class RestaurantListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating restaurants.
    Only owners can create new restaurants.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MenuListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating menus.
    Only owners and employees can create new menus.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(pk=self.request.data['restaurant'])
        if self.request.user.is_owner or self.request.user.is_employee and self.request.user.restaurant == restaurant:
            serializer.save()
        else:
            raise permissions.DjangoPermissionDenied


# Similar views for Category, MenuItem, and Modifier