# permissions.py
from rest_framework import permissions

class IsWarehouseManager(permissions.BasePermission):
    """Allows access only to Warehouse Managers."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Warehouse Manager').exists()

class IsInventoryClerk(permissions.BasePermission):
    """Allows access to clerks for data entry."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Inventory Clerk', 'Warehouse Manager']).exists()