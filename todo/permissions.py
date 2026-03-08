from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    message = "You are already logged in."

    def has_permission(self, request, view):
        return bool(not request.user or request.user.is_anonymous)
