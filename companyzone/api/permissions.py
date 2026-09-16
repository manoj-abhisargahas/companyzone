from rest_framework.permissions import BasePermission

#Ver-02:
class UserPermissionsChecker(BasePermission):
    """
    Checks permissions based on an `permissions_required_actions_map` dict defined on the view.
    Works for:
        ViewSets (via view.action) 
        APIView (via request.method)
        Function-Based Views (via function attributes)
    """
    def has_permission(self, request, view):
        # Extract the action name (lowercase HTTP method for function views)
        action = getattr(view, 'action', request.method.lower())

        # 1. Extract the mapping for class-Based Views
        perms_req_actions_map = getattr(view, 'permissions_required_actions_map', {})

        # Fallback lookup tree to extract view inside a function-based view is an instance of DRF's internal class called WrappedAPIView, 
        # calling getattr(view, ...) actually checks the WrappedAPIView class instance—not your function. 
        # That is why it returns "None", So, we falls back to checking view.callback
        if perms_req_actions_map is None:
            # Look at the view's inner callable attribute (assigned by @api_view decorator)
            # When you use the @api_view decorator, 
            # Django REST Framework does something unique behind the scenes:
            #   It creates an internal, hidden subclass of APIView called WrappedAPIView.
            #   It assigns your original function (e.g., employee_modify_api) as the view.callback attribute on that wrapper object.
            #   It returns this wrapper so Django's routing system can handle it like a standard class-based view.
            callback_func = getattr(view, 'callback', None)
            perms_req_actions_map = getattr(callback_func, 'permissions_required', {})

        perms_required = perms_req_actions_map.get(action, [])

        if not perms_required:
            return False

        return any(request.user.has_perm(perm) for perm in perms_required)


#Ver-01:
class UserPermissionsCheckerVer1(BasePermission):
    """
    Checks permissions based on an `permissions_required_actions_map` dict defined on the view.
    Works for both ViewSets (via view.action) and APIView (via request.method).
    """
    def has_permission(self, request, view):
        # Extract the action name (lowercase HTTP method for function views)
        action = getattr(view, 'action', request.method.lower())
        perms_req_actions_map = getattr(view, 'permissions_required_actions_map', {})
        perms_required = perms_req_actions_map.get(action, [])

        if not perms_required:
            return False

        return any(request.user.has_perm(perm) for perm in perms_required)