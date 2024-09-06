# from rest_framework import permissions
# from .models import Restaurant, Menu, Category, MenuItem, Modifier
# from users.models import User


# class IsOwnerOrEmployeeOfRestaurant(permissions.BasePermission):
#     """
#     Custom permission to allow only owners and employees of a restaurant to access certain views.
#     """
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if view.basename == 'restaurant':
#                 return request.user.is_owner
#             elif view.basename in ['menu', 'category', 'menuitem', 'modifier']:
#                 try:
#                     restaurant = Restaurant.objects.get(pk=request.data['restaurant'])
#                     return request.user.is_owner or (request.user.is_employee and request.user.restaurant == restaurant)
#                 except (Restaurant.DoesNotExist, KeyError):
#                     return False
#         return False

#     def has_object_permission(self, request, view, obj):
#         if isinstance(obj, (Restaurant, Menu, Category, MenuItem, Modifier)):
#             return request.user.is_owner or (request.user.is_employee and request.user.restaurant == obj.restaurant)
#         return False


from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Restaurant, Menu, Category, MenuItem, Modifier


class IsOwnerOrEmployeeOfRestaurant(permissions.BasePermission):
    """
    Custom permission to allow only owners and employees of a restaurant to access certain views.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if it's a restaurant-related request
            if view.basename == 'restaurant':
                return request.user.is_owner  # Only owners can create restaurants

            # Check for menu, category, menuitem, or modifier views
            restaurant = self._get_related_restaurant(request)
            if restaurant:
                return request.user.is_owner or (request.user.is_employee and request.user.restaurant == restaurant)

        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check for restaurant, menu, category, menu item, or modifier.
        """
        restaurant = None
        if isinstance(obj, Restaurant):
            restaurant = obj
        elif isinstance(obj, Menu):
            restaurant = obj.restaurant
        elif isinstance(obj, Category):
            restaurant = obj.menu.restaurant
        elif isinstance(obj, MenuItem):
            restaurant = obj.category.menu.restaurant
        elif isinstance(obj, Modifier):
            restaurant = obj.menu_item.category.menu.restaurant

        return request.user.is_owner or (request.user.is_employee and request.user.restaurant == restaurant)

    def _get_related_restaurant(self, request):
        """
        Helper method to fetch the restaurant related to the request data.
        """
        restaurant_id = request.data.get('restaurant')
        if restaurant_id:
            try:
                return get_object_or_404(Restaurant, pk=restaurant_id)
            except Restaurant.DoesNotExist:
                return None
        return None
