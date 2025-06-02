from rest_framework.permissions import BasePermission

class IsEdgeNodeAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        return getattr(request, "edge_node", None) is not None