from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and 'Admin' in request.user.get_role_name)