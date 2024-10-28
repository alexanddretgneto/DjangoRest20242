# # LittleLemonAPI/permissions.py
# from rest_framework.permissions import BasePermission

# class IsManager(BasePermission):
#     def has_permission(self, request, view):
#         # Defina a lógica de permissão para um gerente
#         return True

# class IsDeliveryCrew(BasePermission):
#     def has_permission(self, request, view):
#         # Defina a lógica de permissão para a equipe de entrega
#         return True

# class IsCustomer(BasePermission):
#     def has_permission(self, request, view):
#         # Defina a lógica de permissão para um cliente
#         return True

# class ReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         # Permitir apenas acesso de leitura
#         return request.method in ['GET']
