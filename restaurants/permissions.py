from rest_framework import permissions
from .models import Restaurant, Menu, Category, MenuItem, Modifier
from users.models import User


class IsOwnerOrEmployeeOfRestaurant(permissions.BasePermission):
    """
    Custom permission to allow only owners and employees of a restaurant to access certain views.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.basename == 'restaurant':
                return request.user.is_owner
            elif view.basename in ['menu', 'category', 'menuitem', 'modifier']:
                try:
                    restaurant = Restaurant.objects.get(pk=request.data['restaurant'])
                    return request.user.is_owner or (request.user.is_employee and request.user.restaurant == restaurant)
                except (Restaurant.DoesNotExist, KeyError):
                    return False
        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, (Restaurant, Menu, Category, MenuItem, Modifier)):
            return request.user.is_owner or (request.user.is_employee and request.user.restaurant == obj.restaurant)
        return False