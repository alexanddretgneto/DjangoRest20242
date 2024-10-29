from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='DeliveryCrew').exists()

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        # Lógica de permissão para um cliente
        return request.user.is_authenticated

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET']
