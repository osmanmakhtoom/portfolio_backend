from rest_framework.permissions import BasePermission


class IsVerifier(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.verified_by == request.user
