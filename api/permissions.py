from rest_framework import permissions

class IsBudgetOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a budget to view, edit, or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # obj represents the individual Budget instance being accessed
        return obj.user == request.user