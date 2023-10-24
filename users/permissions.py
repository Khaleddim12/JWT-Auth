from rest_framework import permissions
from django.contrib.auth.decorators import login_required

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_superuser 
    
class IsUserOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        user_owner = obj  # Assuming the `obj` represents the User object itself
        return user_owner is not None and user_owner == request.user
