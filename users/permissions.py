from rest_framework import permissions
from .models import User


class IsOwnerOrEmployee(permissions.BasePermission):
    """
    Custom permission to allow only owners and employees to access views.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_owner or request.user.is_employee
        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        return request.user.is_owner or request.user.is_employee
