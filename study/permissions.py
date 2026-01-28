from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(name='Manager').exists()


class IsOwner(BasePermission):

    def has_permission(self, request, view):

        return request.user == view.get_object().owner