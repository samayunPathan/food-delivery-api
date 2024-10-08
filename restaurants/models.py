from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    """
    Model for a restaurant
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_restaurants', null=True, blank=True)

    class Meta:
        # Add a unique constraint on name and address
        unique_together = ('name', 'address')

    def __str__(self):
        return self.name


class Menu(models.Model):

    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class Category(models.Model):

    name = models.CharField(max_length=100)
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.menu.name} - {self.name}"


class MenuItem(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='menu_items')

    def __str__(self):
        return self.name


class Modifier(models.Model):
    """
    Menu item modifier, including its name and its associated menu item.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name='modifiers')

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"
