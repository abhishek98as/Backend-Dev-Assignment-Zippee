from rest_framework.permissions import BasePermission, SAFE_METHODS


# this permission is for admin only write access
class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return request.user.role == 'admin'
        return False


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        # safe methods are allowed
        if request.method in SAFE_METHODS:
            return True
        # admin can do anything
        if request.user.role == 'admin':
            return True
        # only owner can modify
        return obj.user == request.user
