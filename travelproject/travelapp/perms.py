from rest_framework import permissions


class OwnerPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user == obj.user)


class AdminPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
