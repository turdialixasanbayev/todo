from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    message = "You are already logged in"

    def has_permission(self, request, view):

        return request.user.is_anonymous


class IsOwner(permissions.BasePermission):
    message = "You do not have permission to access this object"

    def has_object_permission(self, request, view, obj):

        return (
            request.user
            and request.user.is_authenticated
            and obj.user == request.user
        )
