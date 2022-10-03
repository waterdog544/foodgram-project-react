from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_staff
        )


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        if request.user != obj.author:
            return request.method in permissions.SAFE_METHODS
        return (
            request.user == obj.author
            or request.user.is_staff
        )


class IsAdminOrReadOnlyObj(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS
