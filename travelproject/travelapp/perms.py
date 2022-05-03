from rest_framework import permissions


class CommentOwnerPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return request.user == comment.user


class AdminPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
