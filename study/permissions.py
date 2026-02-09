from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Manager').exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'owner') and obj.owner == request.user