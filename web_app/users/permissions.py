from rest_framework.permissions import BasePermission


class SuperuserPermission(BasePermission):
    message = "You don't have permissions to do this"

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser


class UserProfilePermission(BasePermission):
    message = "This is not your account"

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.id == obj.id