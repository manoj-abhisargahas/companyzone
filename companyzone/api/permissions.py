from rest_framework.permissions import BasePermission

class UserPermissionsChecker(BasePermission):
    """
    Checks permissions based on an `permissions_required_actions_map` dict defined on the view.
    Works for both APIView (via request.method) and ViewSets (via view.action).
    """
    def has_permission(self, request, view):
        action = getattr(view, 'action', request.method.lower())
        perms_req_actions_map = getattr(view, 'permissions_required_actions_map', {})
        perms_required = perms_req_actions_map.get(action, [])

        if not perms_required:
            return False

        return request.user.has_perms(perms_required)