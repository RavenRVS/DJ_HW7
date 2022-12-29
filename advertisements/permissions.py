from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator or request.user.groups.filter(name='admin').exists():
            return True
        return False
