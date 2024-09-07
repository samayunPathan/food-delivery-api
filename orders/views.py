from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from users.permissions import IsOwnerOrEmployee
from django.db import transaction


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

    def get_queryset(self):
        user = self.request.user
        if user.is_owner or user.is_employee:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific order.
    Customers can only access their own orders, while owners and employees can access all orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrEmployee]

    def get_queryset(self):
        user = self.request.user
        if user.is_owner or user.is_employee:
            return Order.objects.all()
        return Order.objects.filter(user=user)
