from rest_framework import permissions
from .models import Order
from users.models import User


class IsCustomerOrOwnerEmployee(permissions.BasePermission):
    """
    Custom permission to allow customers to access their own orders, and owners/employees to access all orders.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        else:
            return request.user.is_authenticated and (request.user.is_owner or request.user.is_employee)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Order):
            return obj.customer == request.user or request.user.is_owner or request.user.is_employee
        return False