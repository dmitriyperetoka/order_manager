from rest_framework import permissions


class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff
