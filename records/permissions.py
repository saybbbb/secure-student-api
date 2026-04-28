from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to users in the 'Admin' group.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='Admin').exists()
        )


class IsAdminOrFaculty(BasePermission):
    """
    Allows access to users in either the 'Admin' or 'Faculty' group.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name__in=['Admin', 'Faculty']).exists()
        )


class IsOwnerOrAdminOrFaculty(BasePermission):
    """
    Object-level permission:
    - Admin/Faculty can access any record.
    - Students can only access their own record.
    """
    def has_object_permission(self, request, view, obj):
        # Admin and Faculty can access any record
        if request.user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return True
        # Students can only access their own record
        return obj.owner == request.user
