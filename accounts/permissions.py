from rest_framework.permissions import BasePermission

class IsLeader(BasePermission):
    """
    Allow access only to users whose profile.role == 'leader'
    """
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'profile') and request.user.profile.role == 'leader')

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'profile') and request.user.profile.role == 'employee')
