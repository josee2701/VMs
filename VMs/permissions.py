# your_app/permissions.py
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Solo administradores pueden POST, PUT, DELETE. 
    Clientes (u otros auth'd) solo GET.
    """
    def has_permission(self, request, view):
        # Métodos seguros
        if request.method in permissions.SAFE_METHODS:
            return True
        # Para otros métodos, rol debe ser admin
        return request.user.is_authenticated and request.user.role == 'admin'
