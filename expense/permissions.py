from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    ''' Only Non-Admin Users are Allowed'''
    
    def has_object_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff==False)