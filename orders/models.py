from django.db import models

# Create your models here.
from django.db import models
from restaurants.models import MenuItem, Restaurant
from users.models import User


class Order(models.Model):
    """
    Model for an order, including the customer, restaurant, order items, and payment method.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    payment_method = models.CharField(
        max_length=50, choices=[('card', 'Card'), ('cash', 'Cash')])
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    """
    Model for an item in an order, including the order, menu item, and quantity.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"
