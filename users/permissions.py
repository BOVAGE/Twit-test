from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        give write access only if the views's id is that of the authenticated user 
    """

    def has_permission(self, request, view):
        id = view.kwargs.get('id')
        if request.method in permissions.SAFE_METHODS:
            return True
        return id == request.user.id