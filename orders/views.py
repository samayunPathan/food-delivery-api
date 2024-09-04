from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer
from users.permissions import IsOwnerOrEmployee


class OrderListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating orders.
    Customers can create new orders, while owners and employees can view all orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated(), IsOwnerOrEmployee()]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)